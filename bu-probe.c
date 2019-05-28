/*
*              G O R D O N
* Detecting TCP variants on the internet
*---------------------------------------
*
*           Probe.c      : Base program. Registers nfqueue callback
*			Arguments    : <target>		URL of the target host
*                          <targetFile>	subdomain name/ file to be retrieved
*                          <outFile>    output file for writing cwnd data
*					       <qd>			Queuing delay to be emulated in ns
*
*		    Example		 : sudo iptables -I INPUT -p tcp -s 137.132.83.98 -m state --state ESTABLISHED -j NFQUEUE --queue-num 0
*						   ./prober 100.64.0.2 www.facebook.com none windows.csv 500
*/

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <linux/types.h>
#include <linux/netfilter.h>		/* for NF_ACCEPT */

#include <libnetfilter_queue/libnetfilter_queue.h>
#include <linux/tcp.h>
#include <linux/ip.h>
#include <time.h>
#include <string.h>
#include <pthread.h>
#include <math.h>

int drop = 1;
int acceptWindow = 0;
int dropWindow = 0;
uint dropSeq = 0;
int cap = 500;
int done = 0;
int emuDrop=10000;
int randomDrop=0;
uint32_t randomSeq=0;
int nextVal=0;
char buffSize[6];
int indx = 0;

_Bool waiting=0;

//char buffer [250][6];

char* itoa(int n, char *number) 
{ 
	int digit, i=0, j=0, temp = n;
	i=0;
	while(temp!=0){
		digit = temp%10;
		number[i] = (char) (digit+48);
		temp /= 10;
		i++;
	}
	while(j<i/2){
		temp=number[j];
		number[j]=number[i-j-1];
		number[i-j-1]=temp;
		j++;
	} 
	return number;
} 
/*
void split( char string[], int start, int end){
	char str[10];
	int i=0;
	for(i=0; i<(end-start); i++){
		str[i]=string[start+i];
	}
	strcpy(buffSize, str);
	return;
}

void *keepReading(){
//void keepReading(){
	char filename[] = "/proc/net/netfilter/nfnetlink_queue";
	FILE *file = fopen(filename, "r");

	while(1){
		fseek(file, 0, SEEK_SET);
		if (file != NULL) {
			char stats [60];
			fgets(stats,sizeof stats,file);
			printf("\n%s", stats);
			split(stats, 12, 18); 
		}
	}

}
*/
static int cb(struct nfq_q_handle *qh, struct nfgenmsg *nfmsg,
	      struct nfq_data *nfa, void *data)
{
	unsigned char *pkt;
	struct nfqnl_msg_packet_hdr *header;
	uint32_t id = 0;
	uint32_t tseq = 0;

	header = nfq_get_msg_packet_hdr(nfa);
	id = ntohl(header->packet_id);
	unsigned int ret = nfq_get_payload(nfa, &pkt);
	
	unsigned int by = 0;
	for (int i = 24; i < 28; i++) {
		by = (unsigned int) pkt[i];
		tseq += by << 8*(24-i);
	}

	if(tseq == randomSeq){
		waiting=0;
		return nfq_set_verdict(qh, id, NF_ACCEPT, 0, NULL);
	}
	else if(acceptWindow < cap){
		if(acceptWindow == emuDrop){
			acceptWindow++;
			randomSeq = tseq;
			return nfq_set_verdict(qh, id, NF_DROP, 0, NULL);
		}
		else if(atoi(buffSize)>100 && waiting==0){
			waiting=1;
			acceptWindow++;
			randomSeq = tseq;
			return nfq_set_verdict(qh, id, NF_DROP, 0, NULL);
		}
		else{
			acceptWindow++;
			return nfq_set_verdict(qh, id, NF_ACCEPT, 0, NULL);
		}
	}
	else if(tseq == dropSeq){
		nextVal = acceptWindow + dropWindow;
		done=1;
		return nfq_set_verdict(qh, id, NF_ACCEPT, 0, NULL);
	}
	else{
		if(drop == 1){
			drop=0;
			dropSeq=tseq;
		}
		dropWindow++;
		//printf("%s", buffSize);
		//strcpy(buffer[dropWindow-1],buffSize);
		return nfq_set_verdict(qh, id, NF_DROP, 0, NULL);
	}
}

int main(int argc, char **argv)
{
	struct nfq_handle *h;
	struct nfq_q_handle *qh;
	int fd;
	int rv;
	char buf[4096] __attribute__ ((aligned));
	int lastWindow;
	int inputting = 0;

	char outfile[] = "windows.csv";
	FILE *ofile = fopen(outfile, "rw");

	char line [128]; 
    	while (fgets(line, sizeof line, ofile) != NULL) 
	{
		indx++; 
		lastWindow = atoi(line);
		if(inputting==0){
			if(lastWindow>80){
				emuDrop = lastWindow;
				inputting=1;
			}
		}	
    }
    cap=atoi(line);
	if(cap==0){
		cap=lastWindow;
	}

	h = nfq_open();
	if (!h) {
		//fprintf(stderr, "error during nfq_open()\n");
		exit(1);
	}

	//printf("unbinding existing nf_queue handler for AF_INET (if any)\n");
	if (nfq_unbind_pf(h, AF_INET) < 0) {
		fprintf(stderr, "error during nfq_unbind_pf()\n");
		exit(1);
	}

	//printf("binding nfnetlink_queue as nf_queue handler for AF_INET\n");
	if (nfq_bind_pf(h, AF_INET) < 0) {
		fprintf(stderr, "error during nfq_bind_pf()\n");
		exit(1);
	}

	//printf("binding this socket to queue '0'\n");
	qh = nfq_create_queue(h,  0, &cb, NULL);
	if (!qh) {
		fprintf(stderr, "error during nfq_create_queue()\n");
		exit(1);
	}

	//printf("setting copy_packet mode\n");
	if (nfq_set_mode(qh, NFQNL_COPY_PACKET, 0xffff) < 0) {
		fprintf(stderr, "can't set packet_copy mode\n");
		exit(1);
	}

	fd = nfq_fd(h);

	/*
	pthread_t reader;
	pthread_create( &reader, NULL, keepReading, NULL );
	*/

	int delay=8000;

	//system("wget caprica.d2.comp.nus.edu.sg/test.txt&");
	char get[] ="wget -U mozilla ";
	strcat(get, argv[1]);
	strcat(get,"&");
	//printf("=========================%s", get);
	system(get);

	int counter=0;
 
	while ((rv = recv(fd, buf, sizeof(buf), 0)) && rv >= 0 && done==0){
		usleep(delay);
		nfq_handle_packet(h, buf, rv);
		if(counter>1000) delay=5000;
		counter++;
	}
	
	system("sudo killall wget");
	//printf("Ended wget and tcpdump process.");

	//pthread_cancel(reader);

	//printf("unbinding from queue 0\n");
	nfq_destroy_queue(qh);

	#ifdef INSANE
		/* normally, applications SHOULD NOT issue this command, since
	 	* it detaches other programs/sockets from AF_INET, too ! */
		//printf("unbinding from AF_INET\n");
		nfq_unbind_pf(h, AF_INET);
	#endif

	nfq_close(h);

	fseek(ofile, 0, SEEK_END);
	/*
	for(int i=0; i<dropWindow; i++){
		printf("\n%f ", (indx*1.0)+(i*1.0/dropWindow));
		for (int j=0; j<6; j++){
			printf("%c", buffer[i][j]);
		}
	}
	*/

	char number[5];
	char window[5];
	char in[5];
	char cmd[]="echo ";
	
	//write data to windows.csv
	itoa(nextVal, number);
	strcat(cmd, number);
	strcat(cmd," ");
	itoa(nextVal-acceptWindow, window);
	strcat(cmd, window);
	strcat(cmd," ");
	itoa(indx, in);
	strcat(cmd, in);
	strcat(cmd, " >> windows.csv");
	system(cmd);

	return 0; 
}
