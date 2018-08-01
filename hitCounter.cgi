#!/usr/bin/perl

########################################
#         Frederico Gonçalves          #
#              20/07/2018              #
########################################

use POSIX;
use warnings;
my $fileName = $ARGV[0];
if($fileName eq ''){
	exit;
}

############## CHANGE THIS PATHS ##############
my $tail = '/usr/bin/tail';
my $path = '/opt/apache2/cgi-bin/hitCounter/';
###############################################


my $completePath = $path.$fileName;
my $today = strftime "%d/%m/%Y", localtime;
my $printString = $today.';';

unless (-e $completePath){
	open LOGFILE, '>', $completePath or die "Cannot create file $completePath: $!\n\n";
	print LOGFILE $today.';1';
	close LOGFILE or die "Cannot close file $completePath: $!\n";
}
else{
	open LOGFILE, '+<', $completePath or die "Cannot create file $completePath: $!\n\n";
	flock(LOGFILE, 2) or die "Cannot lock $completePath exclusively: $!";
	my $output = `$tail -1 $completePath`;
	if($output =~ m/$today;([0-9]+)/){
		my $counter = $1+1;
		$printString .= $counter;
		my $length = length($output);
		seek(LOGFILE,-$length,2);
		print LOGFILE $printString;
	}
	else{
		seek(LOGFILE,0,2);
		$printString .= '1';
		print LOGFILE "\n".$printString;
	}
	flock(LOGFILE, 8) or die "Cannot unlock $completePath exclusively: $!";
	close LOGFILE or die "Cannot close file $completePath: $!\n";
}
