"""
Implements action listeners for the menu items

Copyright (c) 2018

:author: J. L. Lawrence
:version 3.0, 2018
"""

import sys

import ASTUtils.ASTAngle as ASTAngle
import ASTUtils.ASTCatalog as ASTCatalog
import ASTUtils.ASTConstellation as ASTConstellation
import ASTUtils.ASTFileIO as ASTFileIO
import ASTUtils.ASTInt as ASTInt
from ASTUtils.ASTMisc import HIDE_ERRORS, HMSFORMAT, DMSFORMAT, DEFAULT_EPOCH, ASCENDING_ORDER
import ASTUtils.ASTMsg as ASTMsg
from ASTUtils.ASTPrt import CENTERTXT
import ASTUtils.ASTQuery as ASTQuery
import ASTUtils.ASTStr as ASTStr
import ASTUtils.ASTTime as ASTTime

import Chap1.ChapEnums

#==================================================
# Define listeners for about, exit, instructions
#==================================================

def aboutMenuListener(gui):
    """
    Handle a click on the About menu item
    
    :param tkwidget gui: GUI that the About Box is associated with
    """
    gui.showAboutBox()
    


def exitMenuListener():
    """Handle a click on the Exit menu item"""
    if ASTMsg.pleaseConfirm("Are you sure you want to exit?"," "):
        sys.exit()    
    


def instructionsMenuListener(prt):
    """
    Handle a click on the Instructions menu item
    
    :param ASTPrt prt: ASTPrt object instance created by the top level GUI
    """
    prt.clearTextArea()
    prt.setBoldFont(True)
    prt.println("Instructions",CENTERTXT)
    prt.setBoldFont(False)
    prt.println()
 
    prt.println("This program allows you to examine constellations and objects in star catalogs in various ways." +
            " If you want the lists of objects to be displayed in ascending order, check the 'Sort in Ascending Order' " +
            " checkbox. If you want to sort in descending order, be sure the checkbox is unchecked.")
    prt.println()
    
    prt.println("The 'Constellations' menu allows you to display information about the 88 modern constellations. You can " +
            "display a list of all the constellations and basic information about them, or use the " +
            "'List a Constellation by ...' menu item to list individual constellations with more detailed information. " +
            "The 'Find Constellation an Object is In' menu item allows you to enter the Right Ascension (in hours) and " +
            "Declination (in degrees) for an object and determine what constellation the object lies within.")
    prt.println()
    
    prt.printnoln("The 'Star Catalogs' menu item allows you to load a star catalog and see basic information about the " +
            "catalog, such as where it came from, how many objects are in the catalog, and what constellations " +
            "those objects are in. The catalogs ")
    prt.setBoldFont(True)
    prt.printnoln("*MUST*")
    prt.setBoldFont(False)
    prt.println(" be in the format specifically designed for the programs in this book. Look at the source code for this " +
            "program, the README.txt file, or any of the star catalog data files to understand the format of the " +
            "star catalog data files. The star catalog data files are ordinary text files in a 'pseudo-XML' format. " +
            "You can download publically available data from some astronomy/space organization to create your own " +
            "star catalog files as long as the data is plain ASCII data in exactly the format this book requires.")
    prt.println()
    
    prt.printnoln("The 'Space Objects' menu allows you to look at objects within an already loaded catalog. You can display " +
            "individual objects by entering their name or alternate name. It is important to note that the name/alternate name " +
            "entered must match a name in the")
    prt.setBoldFont(True)
    prt.printnoln(" *currently loaded* ")
    prt.setBoldFont(False)
    prt.println("catalog because different catalogs (e.g., Messier versus Henry Draper) use different names " +
            "for the same object. The 'List all Space Objects ...' menu entry allows you to " +
            "look at all, or a subset of, the objects in the catalog. For example, if you wish to explore " +
            "the objects within a particular constellation, choose the 'In a Constellation' sub-menu to see " +
            "all objects within the currently loaded catalog that are in a given constellation. Be aware that " +
            "some of the catalogs are quite large and may take considerable time to display all of their objects. " +
            "The 'Sort Catalog by ...' menu item allows you to sort the catalog objects in various ways before " +
            "displaying them.")
    prt.println()
    
    prt.printnoln("Several menu options, such as those under 'List a Catalog Object by ...', allow you to enter a string, " +
            "such as an object name, to search for in the currently loaded catalog. When searches are performed for " +
            "a string that you enter, the search is not case sensitive. Thus, a search for 'm39' and 'M39' will yield " +
            "the same results. Also, spaces are generally not important so that a search for 'M 39' will yield the " +
            "same result as a search for 'M39'.")
    prt.resetCursor()
   


#==================================================
# Define listener for the menu items
#==================================================

def menuListener(calcToDo,gui):
    """
    Handle a click on the menu items
    
    :param CalculationType calcToDo: the calculation to perform
    :param tkwidget gui: GUI object to which menu items are associated)
    """
    cen = Chap1.ChapEnums.CalculationType           # shorten to make typing easier!!!
    
    #****************Constellations Menu
    if (calcToDo == cen.LISTCONSTBYNAME):
        listConstByName(gui)        
    elif (calcToDo == cen.LISTCONSTBYABBREVNAME):
        listConstByAbbrevName(gui)
    elif (calcToDo == cen.LISTCONSTBYMEANING): 
        listConstsByMeaning(gui)
    elif (calcToDo == cen.LISTALLCONST):
        listAllConstellations(gui)
    elif (calcToDo == cen.FINDCONST):
        findConstellationForRA_Decl(gui)

    #****************Star Catalogs Menu
    elif (calcToDo == cen.CLEARCAT):
        clearCatalog(gui)
    elif (calcToDo == cen.LOADCAT):       
        loadCatalog(gui)
    elif (calcToDo == cen.SHOWCATINFO):
        showCatalogInfo(gui)

    #*****************Space Objects Menu
    elif (calcToDo == cen.LISTOBJBYNAME):        
        listObjByName(gui)
    elif (calcToDo == cen.LISTOBJBYALTNAME):    
        listObjByAltName(gui)
    elif (calcToDo == cen.LISTOBJBYCOMMENTS):    
        listObjByComments(gui)
    elif (calcToDo == cen.LISTALLOBJSINCAT):
        listAllObjsInCatalog(gui)
    elif (calcToDo == cen.LISTALLOBJSINRANGE): 
        listAllObjsByRange(gui)
    elif (calcToDo == cen.LISTALLOBJSINCONST): 
        listAllObjsByConst(gui)
    elif (calcToDo == cen.SORTCATBYCONST):
        sortCatalog(gui,ASTCatalog.CatalogSortField.CONSTELLATION)
    elif (calcToDo == cen.SORTCATBYCONSTANDOBJNAME):
        sortCatalog(gui,ASTCatalog.CatalogSortField.CONST_AND_OBJNAME)
    elif (calcToDo == cen.SORTCATBYOBJNAME):
        sortCatalog(gui,ASTCatalog.CatalogSortField.OBJNAME)
    elif (calcToDo == cen.SORTCATBYOBJALTNAME):
        sortCatalog(gui,ASTCatalog.CatalogSortField.OBJ_ALTNAME)
    elif (calcToDo == cen.SORTCATBYOBJRA):
        sortCatalog(gui,ASTCatalog.CatalogSortField.RA)
    elif (calcToDo == cen.SORTCATBYOBJDECL):
        sortCatalog(gui,ASTCatalog.CatalogSortField.DECL)
    elif (calcToDo == cen.SORTCATBYOBJMV):
        sortCatalog(gui,ASTCatalog.CatalogSortField.VISUAL_MAGNITUDE)

    else:           # This should never happen
        ASTMsg.criticalErrMsg("Unimplemented menu item " + str(calcToDo))
        


#=========================================
# Handle Constellations menu items
#=========================================

def findConstellationForRA_Decl(gui):
    """
    Finds the constellation that a given RA/Decl falls within.
    
    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()   

    # Get RA & Decl
    if (ASTQuery.showQueryForm(["Enter Right Ascension (hh:mm:ss.ss) for Epoch 2000.0",
                                "Enter Declination (xxxd yym zz.zzs) for Epoch 2000.0"]) != ASTQuery.QUERY_OK):
        return
    
    strTmp=ASTQuery.getData(1) # RA
    if ((strTmp == None) or (len(strTmp) <= 0)):
        return
    raObj = ASTTime.isValidTime(strTmp,HIDE_ERRORS)
    if not (raObj.isValidTimeObj()):
        ASTMsg.errMsg("The RA entered is invalid - try again.", "Invalid RA")
        return
    
    strTmp=ASTQuery.getData(2) # Decl
    if ((strTmp == None) or (len(strTmp) <= 0)):
        return
    declObj = ASTAngle.isValidAngle(strTmp,HIDE_ERRORS)
    if not (declObj.isValidAngleObj()):
        ASTMsg.errMsg("The Declination entered is invalid - try again.", "Invalid Decl")
        return

    prt.clearTextArea()
    
    idx = ASTConstellation.findConstellationFromCoord(raObj.getDecTime(),declObj.getDecAngle(),DEFAULT_EPOCH)
    
    if (idx < 0):
        ASTMsg.criticalErrMsg("Could not determine a constellation for the data entered.")
    else:
        prt.println("The location "+ASTTime.timeToStr_obj(raObj, HMSFORMAT) + " RA, " +
                    ASTAngle.angleToStr_obj(declObj,DMSFORMAT) + " Decl " +
                    "is in the "+ASTConstellation.getConstName(idx) + " (" +
                    ASTConstellation.getConstAbbrevName(idx)+") constellation")    

    prt.resetCursor()



def listAllConstellations(gui):
    """
    Displays a list of all of the constellations.
    
    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()
    
    prt.clearTextArea()
    prt.setFixedWidthFont()
    ASTConstellation.displayAllConstellations()
    prt.setProportionalFont()
    prt.resetCursor()



def listConstByAbbrevName(gui):
    """
    Displays detailed information about a constellation when
    given its abbreviated name.

    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()

    if (ASTQuery.showQueryForm(["Enter Constellation's 3 Character\nAbbreviated Name"]) != ASTQuery.QUERY_OK):
        return

    sAbbrevName = ASTQuery.getData(1)
    if ((sAbbrevName == None) or (len(sAbbrevName) <= 0)):
        return

    prt.clearTextArea()
    idx = ASTConstellation.findConstellationByAbbrvName(sAbbrevName.strip())
    if (idx < 0):
        prt.println("No Constellation whose abbreviated name is '" + sAbbrevName + "' was found")
    else:
        ASTConstellation.displayConstellation(idx)
    
    prt.resetCursor()



def listConstsByMeaning(gui):
    """
    Displays detailed information about the constellations that contain a target substring
    in their "meaning" field.

    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()
      
    if (ASTQuery.showQueryForm(["Enter Substring to Search for in the\n"+
                                "Constellation's 'Meaning' field"]) != ASTQuery.QUERY_OK):
        return

    targ = ASTQuery.getData(1)
    if ((targ == None) or (len(targ) <= 0)):
        return
    
    prt.clearTextArea()
    
    iResult = ASTConstellation.findConstellationsByMeaning(targ.strip())
    
    n=len(iResult)
    
    if (n <= 0):
        prt.println("No Constellation(s) found with a 'Meaning' field containing the substring '"+targ+"'")
    else:
        # There is at least one constellation to display
        if (n == 1):
            prt.println("One Constellation has the substring '"+targ+"' in it's 'Meaning' field")
        else:
            prt.println(str(n) + " Constellations have the substring '"+targ+"' in their 'Meaning' field")
            
        for i in range(0,n):
            prt.println()
            prt.setFixedWidthFont()
            prt.println("*"*80)
            prt.setProportionalFont()
            prt.println("Constellation # " + str(i+1))
            ASTConstellation.displayConstellation(iResult[i])
    
    prt.resetCursor()



def listConstByName(gui):
    """
    Displays detailed information about a constellation when given its name.
    
    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()

    if (ASTQuery.showQueryForm(["Enter Constellation Name to Display"]) != ASTQuery.QUERY_OK):
        return
    
    sConstName = ASTQuery.getData(1)
    if ((sConstName == None) or (len(sConstName) <= 0)):
        return
     
    prt.clearTextArea()
    
    idx = ASTConstellation.findConstellationByName(sConstName.strip())
    if (idx < 0):
        prt.println("There is no Constellation with the name '"+sConstName+"'")
    else:
        ASTConstellation.displayConstellation(idx)

    prt.resetCursor()



#=========================================
# Handle Star Catalogs menu items
#=========================================

def clearCatalog(gui):
    """
    Clears all catalog data currently loaded.
    
    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()

    if (not ASTCatalog.isCatalogLoaded()):
        ASTMsg.errMsg("No catalog is currently loaded, so there is nothing to clear.", "No Catalog Loaded")
        return
    
    prt.clearTextArea()
    
    if (ASTMsg.pleaseConfirm("Are you sure you want to clear all\ncurrently loaded catalog data?","Clear Catalog Data")):
        ASTCatalog.clearCatalogAndSpaceObjects()
        gui.setFilename("")
        gui.setCatalogType("")
        gui.setEpoch(DEFAULT_EPOCH)
        prt.println("All currently loaded catalog data was cleared ...")
    else:
        prt.println("Catalog data was not cleared ...")
        
    prt.resetCursor()



def loadCatalog(gui):
    """
    Loads a star catalog from disk.
    
    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()

    fileToRead = ASTFileIO.getFileToRead("Select Catalog to Load ...",ASTCatalog.ASTCatalog.getFileExtFilter(),
                                         ASTCatalog.ASTCatalog.getCatDataDir(),"")
    
    if ((fileToRead == None) or (len(fileToRead) <= 0)):
        return
    
    gui.setFilename(fileToRead)
    
    prt.clearTextArea()
    
    if ((ASTFileIO.getFileSize(fileToRead)/1024.0) > ASTCatalog.MAX_CATALOG_FILESIZE_KB):
        ASTMsg.infoMsg("Warning: Due to its size, it may take several seconds to load\n" +
                       "this Star Catalog. Click 'OK' and then please be patient.\n" +
                       "A message will be displayed when loading is completed.","")
    
    if (ASTCatalog.loadFormattedStarCatalog(fileToRead)):
        s = ASTStr.strFormat("Read in %d different Constellations with a total of ",ASTCatalog.getCatNumConst()) +\
            ASTStr.strFormat("%d Objects",ASTCatalog.getCatNumObjs())
        prt.println(s)
        gui.setCatalogType(ASTCatalog.getCatType())
        gui.setEpoch(ASTCatalog.getCatEpoch())
    else:          
        ASTMsg.errMsg("Could not load the catalog data from "+fileToRead, "Catalog Load Failed")
        gui.setFilename("")
        gui.setCatalogType("")
        gui.setEpoch(DEFAULT_EPOCH)
    
    prt.resetCursor()



def showCatalogInfo(gui):
    """
    Shows the catalog information from the currently loaded catalog.
    
    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()
    
    if not (ASTCatalog.isCatalogLoaded()):
        ASTMsg.errMsg("No catalog is currently loaded.", "No Catalog Loaded")
    else:
        prt.clearTextArea()
        ASTCatalog.displayCatalogInfo()
        prt.resetCursor()



#=====================================
# Handle Space Objects menu items
#=====================================

def listAllObjsByConst(gui):
    """
    Shows all space objects within a given constellation.
    
    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance() 

    if (not ASTCatalog.isCatalogLoaded()):
        ASTMsg.errMsg("No catalog is currently loaded.", "No Catalog Loaded")
        return
     
    if (ASTQuery.showQueryForm(["Enter Constellation's 3 Character Abbreviated Name"]) != ASTQuery.QUERY_OK):
        return
     
    constAbbrevName = ASTQuery.getData(1)
    if ((constAbbrevName == None) or (len(constAbbrevName) <= 0)):
        return
     
    prt.clearTextArea()
    
    idx = ASTConstellation.findConstellationByAbbrvName(constAbbrevName.strip())
    if (idx < 0):
        prt.println("No Constellation whose abbreviated name is '" + constAbbrevName + "' was found")
    else:
        prt.setFixedWidthFont()    
        ASTCatalog.displayAllObjsByConstellation(idx,gui.getSortOrderChkbox())        
        prt.setProportionalFont()
        
    prt.resetCursor()



def listAllObjsByRange(gui):
    """
    Shows all space objects within a user specified index range.
    
    :param tkwidget gui: GUI object from which the request came
    """
    iMaxNum = 100                # default to 1st 100 entries
    
    prt = gui.getPrtInstance()    
     
    if (not ASTCatalog.isCatalogLoaded()):
        ASTMsg.errMsg("No catalog is currently loaded.", "No Catalog Loaded")
        return
    
       
    if (ASTQuery.showQueryForm(["Enter index for 1st object to list\n(ex: 1 for 1st object in the catalog)",
                                "Enter number of objects to list\n(ex: 10 for total of 10 objects)"]) != ASTQuery.QUERY_OK):
        return
     
    prt.clearTextArea()
     
    n = ASTInt.isValidInt(ASTQuery.getData(1),HIDE_ERRORS)
    if (n.isValidIntObj()):
        iStart = n.getIntValue() - 1            # 0 base indexing assumed!
    else:
        iStart = 0
     
    n = ASTInt.isValidInt(ASTQuery.getData(2),HIDE_ERRORS)
    if (n.isValidIntObj()):
        iEnd = iStart + n.getIntValue() - 1
    else:
        iEnd = iStart + iMaxNum - 1
    
    prt.setFixedWidthFont()    
    ASTCatalog.displayAllObjsByRange(iStart,iEnd)        
    prt.setProportionalFont()
    prt.resetCursor()



def listAllObjsInCatalog(gui):
    """
    Shows all catalog information, including space objects,
    in the currently loaded catalog.

    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()    
     
    if (not ASTCatalog.isCatalogLoaded()):
        ASTMsg.errMsg("No catalog is currently loaded.", "No Catalog Loaded")
        return
    
    prt.clearTextArea()
    ASTCatalog.displayCatalogInfo()
    prt.setFixedWidthFont()
    prt.println("*"*80)    
    ASTCatalog.displayAllCatalogObjects()        
    prt.setProportionalFont()
    prt.resetCursor()



def listObjByAltName(gui):
    """
    Displays all catalog information about an object given its alternate name.
    
    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()    
     
    if (not ASTCatalog.isCatalogLoaded()):
        ASTMsg.errMsg("No catalog is currently loaded.", "No Catalog Loaded")
        return
    
    if (ASTQuery.showQueryForm(["Enter the Object's Alternate Name"]) != ASTQuery.QUERY_OK):
        return      
     
    searchStr = ASTQuery.getData(1)
    if ((searchStr == None) or (len(searchStr) <= 0)):
        return
    
    prt.clearTextArea()
    idx = ASTCatalog.findObjByAltName(searchStr.strip())
    if (idx < 0):
        prt.println("No object whose alternate name is '" + searchStr + "' was found in the catalog")
    else:
        ASTCatalog.displayFullObjInfo(idx)
        
    prt.resetCursor()



def listObjByComments(gui):
    """
    Displays detailed information about catalog objects that
    contain a target substring in their "comments" field.

    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()    
     
    if (not ASTCatalog.isCatalogLoaded()):
        ASTMsg.errMsg("No catalog is currently loaded.", "No Catalog Loaded")
        return
    
    if (ASTQuery.showQueryForm(["Enter Substring to Search for in the Object's 'Comments' Field"]) != ASTQuery.QUERY_OK):
        return       

    searchStr = ASTQuery.getData(1)
    if ((searchStr == None) or (len(searchStr) <= 0)):
        return
    
    prt.clearTextArea()

    iResult = ASTCatalog.findObjsByComments(searchStr.strip())
    
    n = len(iResult)
    
    if (n <= 0):
        prt.println("No Objects in the current Catalog have the substring '"+searchStr+"' in their 'Comments' field")
    else:
        if (n == 1):
            prt.println("One Object has the substring '"+searchStr+"' in it's 'Comments' field")
        else:
            prt.println(str(n) + " Objects have the substring '"+searchStr+"' in their 'Comments' field")
    
        for i in range(0,n):
            prt.println()
            prt.setFixedWidthFont()
            prt.println("*"*80)
            prt.setProportionalFont()
            prt.println("Object # " + str(i+1))
            ASTCatalog.displayFullObjInfo(iResult[i])

    prt.resetCursor()



def listObjByName(gui):
    """
    Displays all catalog information about an object given its name.
    
    :param tkwidget gui: GUI object from which the request came
    """
    prt = gui.getPrtInstance()    
     
    if (not ASTCatalog.isCatalogLoaded()):
        ASTMsg.errMsg("No catalog is currently loaded.", "No Catalog Loaded")
        return
    
    if (ASTQuery.showQueryForm(["Enter the Object's Name"]) != ASTQuery.QUERY_OK):
        return
    
    searchStr = ASTQuery.getData(1)
    if ((searchStr == None) or (len(searchStr) <= 0)):
        return    
 
    prt.clearTextArea()
    idx = ASTCatalog.findObjByName(searchStr.strip())
    if (idx < 0):
        prt.println("No object named '" + searchStr + "' was found in the catalog")
    else:
        ASTCatalog.displayFullObjInfo(idx)
    
    prt.resetCursor()    



def sortCatalog(gui,sortField):
    """
    Sorts the currently loaded catalog in ascending or descending
    order depending upon the sort checkbox in the GUI.

    :param tkwidget gui: GUI object from which the request came
    :param CatalogSortFiedl sortField      which field to sort on.
    """
    prt = gui.getPrtInstance()
    sortOrder = gui.getSortOrderChkbox()
            
    if (not ASTCatalog.isCatalogLoaded()):
        ASTMsg.errMsg("No catalog is currently loaded.", "No Catalog Loaded")
        return
     
    prt.clearTextArea()
    prt.printnoln("You have elected to sort the catalog in ")
    if (sortOrder == ASCENDING_ORDER):
        prt.printnoln("ascending")
    else:
        prt.printnoln("descending")
    prt.println(" order by " + sortField.toStr()+" ... ")  
    prt.println()
     
    ASTCatalog.sortStarCatalog(sortField,sortOrder)
    prt.println("The catalog has now been sorted ...")
    prt.resetCursor()



#=========== Main entry point ===============
if __name__ == '__main__':
    pass    
