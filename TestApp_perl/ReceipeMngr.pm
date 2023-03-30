
#-------------------------------------------------------------------------------------------#
# Description: Layout for tables
# Author:SPR
#-------------------------------------------------------------------------------------------#
package TestApp::ReceipeMngr;

#3th party library
use strict;
use warnings;

#local library

sub new {
	my $class = shift;

	my $self = {};
	bless $self;

	$self->{"receipe"} = Receipe->new();

	return $self;
}

#-------------------------------------------------------------------------------------------#
#  Public method
#-------------------------------------------------------------------------------------------#

sub Build {
	my $self = shift;

	die "Build is not implemented";

}

sub Load {
	my $self = shift;

	die "Load is not implemented";

}

sub Store {
	my $self = shift;

	die "Store is not implemented";

}

sub OnBuildReceipeHandler {
	my $self    = shift;
	my $receipe = shift;    # object of helper Receipe class

	# Example user definition of products

	# Build product A (copper)
	my $prodcutA = $receipe->AddProduct("A");
	$prodcutA->AddOpCustom("test operation 1");
	$prodcutA->AddOpCustom("test operation 2");
	$prodcutA->AddOpCustom("test operation 3");

	# Build product B (laminate)
	my $prodcutB = $receipe->AddProduct("B");
	$prodcutB->AddOpCustom("test operation 1");
	$prodcutB->AddOpLaminate($prodcutA);    # merge to receipe together by laminating operation
	$prodcutB->AddOpCustom("test operation 3");

	# Build product C (Kapton)
	my $prodcutC = $receipe->AddProduct("C");
	$prodcutC->AddOpCustom("test operation 1");
	$prodcutC->AddOpCustom("test operation 2");

	# Build product D (laminate)
	my $prodcutD = $receipe->AddProduct("D");
	$prodcutD->AddOpCustom("test operation 1");
	$prodcutB->AddOpLaminate($prodcutC);    # merge to receipe together by laminating operation
	$prodcutD->AddOpCustom("test operation 3");

	# Build product E (Kapton)
	my $prodcutE = $receipe->AddProduct("E");
	$prodcutE->AddOpCustom("test operation 1");
	$prodcutE->AddOpCustom("test operation 2");

	# Build product F (Tape)
	my $prodcutF = $receipe->AddProduct("F");
	$prodcutF->AddOpCustom("test operation 1");
	$prodcutF->AddOpCustom("test operation 2");

	# Build product G
	my $prodcutG = $receipe->AddProduct("G");
	$prodcutG->AddOpCustom("test operation 1");
	$prodcutG->AddOpCustom("test operation 2");
	$prodcutG->AddOpPressing( $prodcutB, $prodcutD );    # merge to receipe together by pressing operation
	$prodcutG->AddOpCustom("test operation 4");
	$prodcutB->AddOpLaminate($prodcutE);                 # merge to receipe together by laminating operation
	$prodcutG->AddOpCustom("test operation 5");
	$prodcutB->AddOpLaminate($prodcutF);                 # merge to receipe together by laminating operation
	$prodcutG->AddOpCustom("test operation 6");

}



#-------------------------------------------------------------------------------------------#
#  Private method
#-------------------------------------------------------------------------------------------#

1;

