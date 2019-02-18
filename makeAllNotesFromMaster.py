
import re
import nbformat
import nbconvert

## TODOs:
### pass AssignmentNumber as argument to this python program
### later add CourseID, CourseName and Course Instance as additional args

def addCourseDetails(NB, CourseID='1MS926', CourseName='Applied Statistics',
                         CourseInstance='Spring 2019, Uppsala University') :
    '''Add Course Details to the Master Notebook NB'''
    #NB['metadata']['lx_assignment_number']=AssignmentNumber
    NB['metadata']['lx_course_number']=CourseID
    NB['metadata']['lx_course_name']=CourseName
    NB['metadata']['lx_course_instance']=CourseInstance
    md = '''# [{}](https://lamastex.github.io/scalable-data-science/as/2019/)\
\n## {}, {} \n&copy;2019 Raazesh Sainudiin. [Attribution 4.0 International \
(CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)'''\
.format(CourseName,CourseID,CourseInstance)
    newCell = nbformat.v4.new_markdown_cell(md)
    newCell['metadata']['deletable']=False
    NB['cells'].insert(0,newCell)
    return NB

def parseCommentMarksIntoMDAndMetaData(NB):
    '''take master NB and turn the #PROBLEM x, #POINT y, #TEST x into md cells
        ADD PROBLEM number in cell metadata
        TODO? make dictionary of points scored, etc.'''
    cellIndex=-1
    AssnProbDict={}
    indicesToInsertCells=[]
    for C in NB['cells']:
        cellIndex=cellIndex+1
        s = C['source']
        sSplitByNewLines = s.split('\n')
        l0=sSplitByNewLines[0] # first line
        sAllButl0 = '\n'.join(sSplitByNewLines[1:]) # gives '' if no extra lines are there
        matchObj = re.match(r'#\s*(\w+)\s+(\d+),\s*(\w+)\s+(\d+),\s*(\w+)\s*(\d+)', l0, re.U)
        if matchObj:
            #print cellIndex, l0
            assignmentNum = str(int(matchObj.group(2)))
            LX_Prob_CellType = matchObj.group(3)
            probNum=str(int(matchObj.group(4)))
            probPoints=str(int(matchObj.group(6)))
            C['metadata']['lx_assignment_number']=assignmentNum
            C['metadata']['lx_problem_cell_type']=LX_Prob_CellType
            C['metadata']['lx_problem_number']=probNum
            C['metadata']['lx_problem_points']=probPoints
            if (LX_Prob_CellType == 'PROBLEM'):
                C['source'] = sAllButl0 # remove first comment line containing PROBLEM
                if assignmentNum+'_'+probNum not in AssnProbDict:
                    md='''---\n---\n## Assignment {}, Problem {}\nMaximum Points = {}'''.format(assignmentNum,probNum,probPoints)
                    newCell = nbformat.v4.new_markdown_cell(md)
                    newCell['metadata']['lx_problem_cell_type']=LX_Prob_CellType
                    newCell['metadata']['lx_assignment_number']=assignmentNum
                    indicesToInsertCells.append([cellIndex,newCell])
                    cellIndex=cellIndex+1
                    AssnProbDict[assignmentNum+'_'+probNum]=1
    # now insert the md cells at the right places
    for iC in indicesToInsertCells:
        NB['cells'].insert(iC[0],iC[1])
    return NB

def addGenericAssignmentAndCourseHeader(NB,AssNum):
    '''Add generic Header for Assignment Number AssNum to input NB'''
    NB['metadata']['lx_assignment_number']=AssNum
    CourseID=NB['metadata']['lx_course_number']
    md = '''# Assignment {} for Course {}\nFill in your Personal Number, make \
    sure you pass the `# ... Test` cells and\n submit by email with *Subject line* \
    **{} Assignment{}**.\nYou can submit multiple times before the deadline \
    and your highest score will be used.'''.format(AssNum,CourseID,CourseID,AssNum)
    newCell = nbformat.v4.new_markdown_cell(md)
    newCell['metadata']['deletable']=False
    NB['cells'].insert(1,newCell)
    return NB

def addStudentIdAtBeginning(NB):
    '''Add a non-Deletable Cell with Student Person Number'''
    newCell = nbformat.v4.new_code_cell('''# Enter your 12 digit personal number here and evaluate this cell\nMyPersonalNumber = 'YYYYMMDDXXXX'\n\n#tests\nassert(isinstance(MyPersonalNumber, basestring))\nassert(MyPersonalNumber.isdigit())\nassert(len(MyPersonalNumber)==12)''')
    newCell['metadata']['lx_cell_type']='personal_number'
    newCell['metadata']['deletable']=False
    NB['cells'].insert(2,newCell)
    return NB

# make a student lab/lecture nb called 01.ipynb
def makeStudentLabLecNotebookWithoutSOLUTIONandTEST(NB):
    '''remove TEST, SOLUTION cells'''
    studentCells=[]
    for C in NB['cells']:
        appendCell=True
        if 'lx_problem_cell_type' in C['metadata']:
            probCellType = C['metadata']['lx_problem_cell_type']
            if ( ("SOLUTION" in probCellType) or ("TEST" in probCellType) ):
                appendCell=False
        if appendCell:
            studentCells.append(C)
    NB['cells']=studentCells
    return NB

def makeStudentAssignmentNotebookWithProblemsAndWithoutSOLUTIONandTEST(NBList,AssNum):
    '''remove TEST, SOLUTION cells and only make PROBLEMs and Self-Test cells of Assignment AssNum'''
    # to create assignments from the master notebook
    NB0=NBList[0].copy()
    NB0 = addGenericAssignmentAndCourseHeader(NB0,AssNum) # Add generic but Assignment/course-specific header
    NB0 = addStudentIdAtBeginning(NB0) # Add Student ID Cell
    studentCells=NB0['cells'][0:3]
    for NB in NBList:
        for C in NB['cells']:
            appendCell=False
            assignmentNumber=''
            probCellType=''
            if 'lx_assignment_number' in C['metadata']:
                assignmentNumber = C['metadata']['lx_assignment_number']
                if assignmentNumber==AssNum:
                    appendCell=True
            if 'lx_problem_cell_type' in C['metadata']:
                probCellType = C['metadata']['lx_problem_cell_type']
                if ( ("SOLUTION" in probCellType) or ("TEST" in probCellType) ):
                    appendCell=False
            if appendCell:
                studentCells.append(C)
        NB0['cells']=studentCells
    return NB0


def makeStudentAssignmentNotebookWithProblemsAndWithSOLUTION(NBList,AssNum):
    '''keep SOLUTION cells as well as PROBLEMs and Self-Test cells of Assignment AssNum'''
    # to create assignments from the master notebook
    NB0=NBList[0].copy()
    NB0 = addGenericAssignmentAndCourseHeader(NB0,AssNum) # Add generic but Assignment/course-specific header
    NB0 = addStudentIdAtBeginning(NB0) # Add Student ID Cell
    studentCells=NB0['cells'][0:3]
    for NB in NBList:
        for C in NB['cells']:
            appendCell=False
            assignmentNumber=''
            probCellType=''
            if 'lx_assignment_number' in C['metadata']:
                assignmentNumber = C['metadata']['lx_assignment_number']
                if assignmentNumber==AssNum:
                    appendCell=True
            if 'lx_problem_cell_type' in C['metadata']:
                probCellType = C['metadata']['lx_problem_cell_type']
                if ("SOLUTION" in probCellType): # not putting TEST cells or ("TEST" in probCellType) ):
                    appendCell=True
            if appendCell:
                studentCells.append(C)
        NB0['cells']=studentCells
    return NB0

def makeStudentVersionsFromMasterNotebookNumbers(inputMasterNBNos):
    for inputMasterNBNum in inputMasterNBNos:
        inputMasterNB=inputMasterNBNum+'.ipynb'
        #read master notebook
        nb = nbformat.read('master/jp/'+inputMasterNB, as_version=4)
        nb = addCourseDetails(nb)
        nb = parseCommentMarksIntoMDAndMetaData(nb)
        #nbformat.write(nb,'master/jp/01_processed.ipynb')
        # to output the course lab/lecture notebook by removing solutions from Assignment01_master
        nb2019jp = makeStudentLabLecNotebookWithoutSOLUTIONandTEST(nb)
        nbformat.write(nb2019jp,'2019/jp/'+inputMasterNB)

def extractAssignmentFromMasterNotebookNumbers(inputMasterNBNos, AssNum):
    '''extract assignment num AssNum from list of master notebook numbers'''
    masterNotebooks=[]
    for inputMasterNBNum in inputMasterNBNos:
        inputMasterNB=inputMasterNBNum+'.ipynb'
        #read master notebook
        nb = nbformat.read('master/jp/'+inputMasterNB, as_version=4)
        nb = addCourseDetails(nb)
        nb = parseCommentMarksIntoMDAndMetaData(nb)
        masterNotebooks.append(nb)
    nb2019jpAss = makeStudentAssignmentNotebookWithProblemsAndWithoutSOLUTIONandTEST(masterNotebooks,AssNum)
    nbformat.write(nb2019jpAss,'2019/jp/Assignment0'+AssNum+'.ipynb')

def extractAssignmentWithSolutionsFromMasterNotebookNumbers(inputMasterNBNos, AssNum):
    '''extract assignment num AssNum from list of master notebook numbers'''
    masterNotebooks=[]
    for inputMasterNBNum in inputMasterNBNos:
        inputMasterNB=inputMasterNBNum+'.ipynb'
        #read master notebook
        nb = nbformat.read('master/jp/'+inputMasterNB, as_version=4)
        nb = addCourseDetails(nb)
        nb = parseCommentMarksIntoMDAndMetaData(nb)
        masterNotebooks.append(nb)
    nb2019jpAss = makeStudentAssignmentNotebookWithProblemsAndWithSOLUTION(masterNotebooks,AssNum)
    nbformat.write(nb2019jpAss,'2019/jp/Assignment0'+AssNum+'_soln.ipynb')


inputMasterNBNos=['00','01','02','03','04']

# make student versions of the notebooks from master notebooks in list above
makeStudentVersionsFromMasterNotebookNumbers(inputMasterNBNos)

# make a student assignment nb called Assignment01.ipynb
extractAssignmentFromMasterNotebookNumbers(inputMasterNBNos, '1')

# make a student assignment nb with solution called Assignment01_soln.ipynb
extractAssignmentWithSolutionsFromMasterNotebookNumbers(inputMasterNBNos, '1')


