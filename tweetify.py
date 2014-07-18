#load string of text
#examine in chunks of 140 characters
#if no sentence-enders (delimiters) exist, chunk into one tweet
#else put as many characters as possible up until the last sentence-ender, chunk into one tweet
#loop

class Tweet:
	def __init__(self, contents="", length=-1):
		self.text = contents
		self.size = length

	def getText(self):
		return self.text
		
	def getSize(self):
		return self.size

def debugIt(debugString):
	if (False):
	#if (True):
		print debugString

def main():
	print "Enter file name: "
	fileName = raw_input()
	with open(fileName, 'r') as f:
		text = f.read()
	f.closed

	primarySplitters = ["!","?",".",",",";","-","\n"]
	secondarySplitAfter = ["}", ")","]",">"]
	secondarySplitBefore = ["{","(","[","<",]
	tertiarySplitters = [" ",]
	tweets = [] #an array to hold our tweets

	startIndex = 0
	while (startIndex < len(text)):
		primaryIndex = secondaryBeforeIndex = secondaryAfterIndex = tertiaryIndex = 141
		
		while (text[startIndex]==" "): #throw away spaces at the start of tweets
			startIndex+=1
		textChunk = text[startIndex:startIndex+140]
		reversedChunk = textChunk[::-1]
		
		debugIt("\n~~~The Text~~~")
		debugIt(textChunk)
		debugIt("~~~End of The Text~~~\n")
		
		for primarySplitter in primarySplitters:
			try:
				tempIndex = reversedChunk.index(primarySplitter)
				if (tempIndex < primaryIndex):
					primaryIndex=tempIndex
			except ValueError:
				pass
				debugIt("\tNo "+primarySplitter+" exists in this string")
		
		for secondarySplitter in secondarySplitAfter:
			try:
				tempIndex = reversedChunk.index(secondarySplitter)
				if (tempIndex < secondaryAfterIndex):
					secondaryAfterIndex=tempIndex
			except ValueError:
				pass
				debugIt("\tNo "+secondarySplitter+" exists in this string")

		for secondarySplitter in secondarySplitBefore:
			try:
				tempIndex = reversedChunk.index(secondarySplitter)
				if (tempIndex < secondaryBeforeIndex):
					secondaryBeforeIndex=tempIndex
			except ValueError:
				pass
				debugIt("\tNo "+secondarySplitter+" exists in this string")
				
		for tertiarySplitter in tertiarySplitters:
			try:
				tempIndex = reversedChunk.index(tertiarySplitter)
				if (tempIndex < tertiaryIndex):
					tertiaryIndex=tempIndex
			except ValueError:
				pass
				debugIt("\tNo "+secondarySplitter+" exists in this string")
		
		#We would rather split for a primary if it wasn't too many characters behind the secondary/tertiary
		#We would rather split for a secondary if it wasn't too many characters behind the tertiary.
		primaryBias = 7 #allow a tweet to end up to 7 characters earlier than another split if there is a primary splitter
		secondaryBias = 4 #allow a tweet to end up to 3 characters earlier than another split if it is secondary, not tertiary
		secondaryBeforeIndex-=1 #we want to split right before these characters, not after them.
		
		if (primaryIndex < primaryBias):
			#we have a primary index within the guaranteed preference range. Use this one!
			bestSplitIndex = primaryIndex
		elif ((secondaryAfterIndex < secondaryBias) or (secondaryBeforeIndex < secondaryBias)):
			#we have a secondary index within the guaranteed preference range. Use this one!
			bestSplitIndex = min(secondaryAfterIndex,secondaryBeforeIndex)
		else:
			#just find the best split.
			bestSplitIndex = min(primaryIndex,secondaryAfterIndex,secondaryBeforeIndex,tertiaryIndex)
		
		normalizedBestSplitIndex = 140-bestSplitIndex
		bestChunk = text[startIndex:startIndex+normalizedBestSplitIndex]
		#print "Characters used:",startIndex, "-",startIndex+normalizedBestSplitIndex
		
		tweets.append(Tweet(bestChunk,len(bestChunk)))
		
		debugIt("\n~~~The Tweet~~~")
		debugIt(tweets[-1].getText())
		debugIt("~~~End of The Tweet~~~\n")
		startIndex+=normalizedBestSplitIndex

	fileNamePrefix = fileName.split(".")[0]
	fileNameSuffix = fileName.split(".")[1]
	with open(fileNamePrefix+"-tweetified"+"."+fileNameSuffix, 'w') as fw:
		i=0
		fw.write("Total number of tweets: "+str(len(tweets))+"\n")
		for tweet in tweets:
			fw.write("Tweet #"+str(i)+": ")
			fw.write(tweet.getText())
			fw.write("\n\n")
			i+=1
	f.closed

main()