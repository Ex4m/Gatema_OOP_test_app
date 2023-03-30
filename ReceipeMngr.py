#-------------------------------------------------------------------------------------------#
# Description: Layout for tables
# Author:SPR
#-------------------------------------------------------------------------------------------#
import Receipe

class ReceipeMngr:
    def __init__(self):
        self.receipe = Receipe()

    #-------------------------------------------------------------------------------------------#
    #  Public method
    #-------------------------------------------------------------------------------------------#

    def Build(self):
        raise NotImplementedError("Build is not implemented")

    def Load(self):
        raise NotImplementedError("Load is not implemented")

    def Store(self):
        raise NotImplementedError("Store is not implemented")

    def OnBuildReceipeHandler(self, receipe):
        # Example user definition of products

        # Build product A (copper)
        prodcutA = receipe.AddProduct("A")
        prodcutA.AddOpCustom("test operation 1")
        prodcutA.AddOpCustom("test operation 2")
        prodcutA.AddOpCustom("test operation 3")

        # Build product B (laminate)
        prodcutB = receipe.AddProduct("B")
        prodcutB.AddOpCustom("test operation 1")
        prodcutB.AddOpLaminate(prodcutA)    # merge to receipe together by laminating operation
        prodcutB.AddOpCustom("test operation 3")

        # Build product C (Kapton)
        prodcutC = receipe.AddProduct("C")
        prodcutC.AddOpCustom("test operation 1")
        prodcutC.AddOpCustom("test operation 2")

        # Build product D (laminate)
        prodcutD = receipe.AddProduct("D")
        prodcutD.AddOpCustom("test operation 1")
        prodcutB.AddOpLaminate(prodcutC)    # merge to receipe together by laminating operation
        prodcutD.AddOpCustom("test operation 3")

        # Build product E (Kapton)
        prodcutE = receipe.AddProduct("E")
        prodcutE.AddOpCustom("test operation 1")
        prodcutE.AddOpCustom("test operation 2")

        # Build product F (Tape)
        prodcutF = receipe.AddProduct("F")
        prodcutF.AddOpCustom("test operation 1")
        prodcutF.AddOpCustom("test operation 2")

        # Build product G
        prodcutG = receipe.AddProduct("G")
        prodcutG.AddOpCustom("test operation 1")
        prodcutG.AddOpCustom("test operation 2")
        prodcutG.AddOpPressing(prodcutB, prodcutD)    # merge to receipe together by pressing operation
        prodcutG.AddOpCustom("test operation 4")
        prodcutB.AddOpLaminate(prodcutE)             # merge to receipe together by laminating operation
        prodcutG.AddOpCustom("test operation 5")
        prodcutB.AddOpLaminate(prodcutF)             # merge to receipe together by laminating operation
        prodcutG.AddOpCustom("test operation 6")
