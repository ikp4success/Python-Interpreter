#!/usr/bin/python
#Group Name: Immanuel I George
#Objective: Build an intepreter program using python

import re
import sys

print('Interpreter Program');
stmtArray = [];
tokenList = [];
data={};
file=open(sys.argv[1],"r");

def stmtlist():
	out = file.readlines();#read statement from file line by line
	for stmt in out:
		if(isEmpty(stmt)==False):#check is stament is empty
			if("print" in stmt or "=" in stmt):#check to see if stament contains print or '='
				if(typeError(stmt)==False): #checking for type error
					stmtArray.append(stmt);
				else:
					print ("Statement is invalid");
		else:
			print ("Statement is invalid");
	return stmtArray;

def isEmpty(stmt):#checking if its empty
	if(stmt==""):
		return True
	else:
		return False
	

def typeError(stmt):
	for eachChar in lex(stmt):
		if(re.search(r'\d+', eachChar)):
			if(isinstance(int(eachChar),int)==True):#checks if its an int
				return False
			else:
				return True
		elif(re.search(r'\d+\.?\d', eachChar)):#checks if its a float
			if(isinstance(float(eachChar),float)==True):
				return False
			else:
				return True		
	

def lex(stmt):

	if("print" in stmt):
		stmtkey = stmt.split(" ")[0]; #returns print
		tokenList.append(stmtkey);
			
		stmt2 = stmt.split("print")[1];#returns anything after print
		for index in range(len(stmt2)):
			tokenList.append(stmt2[index]);#add each character to tokenList
	elif("print" not in stmt):
		stmtkey = stmt.split("=")[0];#returns print
		tokenList.append(stmtkey);
		stmt2 = stmt.split("=")[1];#returns anything after print
		for index in range(len(stmt2)):
			tokenList.append(stmt2[index]);#add each character to tokenList
	return tokenList;

def evaluatePrint(stmtln):
	 if(stmtln.find(";") > -1):
	 	stmtln2 = stmtln.split(" ;")[0]; # removes ';' sign at the end of each statement
	 	printexpr = stmtln2[6:]; # gets substring without print on it, like it strips the print out of stmt
	 	print (Evaluate(printexpr));
	 else:
	 	print ("Statement is invalid"); # Statement is Invalid if it does not have the ';' sign

def evaluateId(stmtln):
	if(stmtln.find(";") > -1):
		stmtln2 = stmtln.split(";")[0]; # removes ';' sign at the end of each statement
		print (Evaluate(stmtln2));
	else:
		print ("Statement is invalid"); # Statement is Invalid if it does not have the ';' sign

def term(passedNum):
	if(re.search(r"\d* \* \d*", passedNum)):
		matchObj = re.search(r"(\w*) \* (\w*)", passedNum);
		factor1 = matchObj.groups()[0];
		factor2 = matchObj.groups()[1];
	
		product = Evaluate(factor1) * Evaluate(factor2);
		
		newExpression = passedNum.replace(factor1 + " * " +  factor2, str(product));
		
		return Evaluate(newExpression)
	elif(passedNum.find(" / ") > - 1):
		location = passedNum.find(" / ");
		addend1 = passedNum[:location];
		addend2 = passedNum[(location + 3):];
		return Evaluate(addend1) / Evaluate(addend2);
	else:
		raise SyntaxError('term() called but number is not multiply or divide.')

def expr(passedNum):
	if(passedNum.find(" + ") > - 1):
			location = passedNum.find(" + ");
			addend1 = passedNum[:location];
			addend2 = passedNum[(location + 3):];
			return Evaluate(addend1) + Evaluate(addend2);
	elif(passedNum.find(" - ") > - 1):
			location = passedNum.find(" - ");
			addend1 = passedNum[:location];
			addend2 = passedNum[(location + 3):];
			return Evaluate(addend1) - Evaluate(addend2);
	else:
		raise SyntaxError('expr() called but number is not multiply or divide.')

def factor(passedNum):
	matchObjf = re.findall(r"\((.+?)\)", passedNum); # strip stament for paranthesis and return expression without paranthesis
	exprwp = matchObjf[0];
	expr2 = "(" + exprwp + ")"
	newexprWP = passedNum.replace(expr2,str(Evaluate(exprwp)));
	
	return Evaluate(newexprWP);

def Evaluate(expression):#print s * t ;
	if (expression.find("=") > -1):
		id = expression.split("=")[0].strip(); #strip out '=' and assign value before '=' as an id	
		value = expression.split("=")[1]; #strip out '=' and assign value after '=' as value
		data[id] = Evaluate(value); # stores the evaluation of value in data, so s = 2 + 3 returns {s,5}
	elif ((re.search('\((.+?)\)', expression))): # check if statment contains open and close paranthesis
		return factor(expression)
	elif (re.search(r"\d* \* \d*", expression) or (expression.find(" / ") > - 1)): # check is its a multiplication/division with two values at each side of it i.e its looking for e.g 2 * 3
	   	return term(expression)
	elif ((expression.find(" + ") > - 1) or (expression.find(" - ") > - 1)): # check if it contains addition or subtraction
		return expr(expression)
	else:
		try:
			value = int(expression);
			return value;#returns int value to value, if there is an error then its a key(i.e print or s or t) or float and not an int
		except ValueError:
			id = expression.split("=")[0];
			printexpr = expression[6:];
			if (id in data):#return value for unknown variable like s=2+3 returns the value for s which was already stored in data dict
				return data.get(id);
			else:
				try:
					value = float(expression);
					return value;#returns float value to value
				except ValueError:
					print ("Statement is invalid");
#Main method
def stmt():
	for stmtln in stmtlist():
		if(stmtln.find("print")>-1):
			evaluatePrint(stmtln);#send statments containing print for evaluation
		if(stmtln.find("=")>-1):
			evaluateId(stmtln);#send statments withou print for evaluation

stmt();
