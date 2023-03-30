#!/usr/bin/perl

#-------------------------------------------------------------------------------------------#
# Description: Script load receipe from disc and test it
# Author:<name>
#-------------------------------------------------------------------------------------------#

# library
use strict;
use warnings;
use aliased 'TestApp::ReceipeMngr';
use aliased 'TestApp::ReceipeTester';

my $receipeMngr = ReceipeMngr->new();    # init manager

# Build user defined receipe
my $receipe = $receipeMngr->Load();
if ( defined $receipe ) {

	# 1) Remove 3rd operation in Product A
	# (so receipe object structure is affected in memory only, not on disc)
	ReceipeTester->RemoveOpByOrder( $receipe, "A", 3 );

	# 2) Test method 1
	ReceipeTester->PrintPressCount($receipe);

	# 3) Test method 2
	ReceipeTester->PrintMaxDepth($receipe);

	# 4) Test method 3
	ReceipeTester->PrintProductPath( $receipe, "A" );

	# 5) Print visualized receipe structure
	ReceipeTester->PrintReceipeTree( $receipe );
	
	# 6) Print receipe to text files
	ReceipeTester->ReceipeOutput( $receipe );

}
else {

	print "Load failed";
}
