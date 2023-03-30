#!/usr/bin/perl

#-------------------------------------------------------------------------------------------#
# Description: Script which build user receipe and store on disc
# Author:<name>
#-------------------------------------------------------------------------------------------#

# library
use strict;
use warnings;
use aliased 'TestApp::ReceipeMngr';

my $receipeMngr = ReceipeMngr->new();    # init manager

# Build user defined receipe
if ( $receipeMngr->Build() ) {

	# Store receipe on disk in JSON/XML
	$receipeMngr->Store();

	print "Build sucess";

}
else {

	print "Build failed";
}
