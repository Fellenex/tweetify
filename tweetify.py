#Loads a file of text and chunks it into tweets based on sentence-enders, or other punctuation delimiters.
#Then, saves the text in tweetified form.

import os
import matplotlib.pyplot as plt

primarySplitters = ["!","?",".",",",";","-","\n"]
secondarySplitAfter = ["}",")","]",">"]
secondarySplitBefore = ["{","(","[","<"]
tertiarySplitters = [" "]

SPLITTERS = [primarySplitters, secondarySplitAfter, secondarySplitBefore, tertiarySplitters]

#We would rather split for a primary if it wasn't too many characters behind the secondary/tertiary
#We would rather split for a secondary if it wasn't too many characters behind the tertiary.
PRIMARY_BIAS = 100	 #allow a tweet to end earlier if there is a good primary splitter
SECONDARY_BIAS = 50	 #allow a tweet to end earlier if there is a good secondary splitter

DEBUG = False
TWEET_LENGTH = 280

def debugIt(debugString):
	if DEBUG: print(debugString)

def main():
	#Get filename from user
	print("Enter file name: ")
	fileName = input()
	with open(fileName, 'r') as f:
		originalText = f.read()
	assert(f.closed)

	tweets = [] #a list to hold our tweets

	startIndex = 0
	while (startIndex < len(originalText)):
		#throw away whitespace at the start of tweets
		while (originalText[startIndex]==" "):
			startIndex+=1

		#We examine the reversed chunk of text because list.index returns the first occurrence.
		reversedChunk = originalText[startIndex:startIndex+TWEET_LENGTH][::-1]

		potentialIndices = []
		for i in range(len(SPLITTERS)):
			#Make a list of indices for each list of splitter characters
			potentialIndices.append([])
			for splitChar in SPLITTERS[i]:

				if splitChar in reversedChunk:
					potentialIndices[i].append(TWEET_LENGTH - reversedChunk.index(splitChar))

		debugIt("Potential indices: "+str(potentialIndices))

		#Get the best index from each list of splitter characters
		bestIndices = []
		for i in potentialIndices:
			bestIndices.append(max(i+[0])) #don't take indices for characters that don't exist

		debugIt("Best indices: "+str(bestIndices))

		#Get the best chunk based on the biases for each type of splitting character
		if bestIndices[0] >= TWEET_LENGTH - PRIMARY_BIAS:
			bestEndingIndex = bestIndices[0]

		elif bestIndices[1] >= TWEET_LENGTH - SECONDARY_BIAS:
			bestEndingIndex = bestIndices[1]

		elif bestIndices[2] >= TWEET_LENGTH - SECONDARY_BIAS:
			#We've found a secondary starting split character (like an opening paren), so we offset by -1
			bestEndingIndex = bestIndices[2] - 1

		else:
			#If we haven't found any splitting characters, then we just split by space. Offset by -1 to exclude the space
			bestEndingIndex = bestIndices[3] - 1

		debugIt("best index: "+str(bestEndingIndex))

		tweets.append(originalText[startIndex : startIndex + bestEndingIndex])

		#Move the starting index forward for the next tweet
		startIndex += bestEndingIndex

	#Save a .txt with the text split up into tweets
	fileNamePrefix = fileName.split(".")[0]
	fileNameSuffix = fileName.split(".")[1]
	with open(fileNamePrefix+"-tweetified"+"."+fileNameSuffix, 'w') as fw:
		i=0
		fw.write("Converted %s characters turned into %s tweets\n" % (len(originalText), len(tweets)))
		for tweet in tweets:
			fw.write("Tweet #"+str(i)+": ")
			fw.write(tweet)
			fw.write("\n\n")
			i+=1
	assert(f.closed)

	plt.hist([len(x) for x in tweets])
	plt.xlabel("Tweet Length (in characters)")
	plt.ylabel("Frequency")
	plt.savefig(fileNamePrefix+"-histogram"+".png")

main()
