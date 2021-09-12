#Generalised Chatbot     
#Don't forget to paste without spacing! (Refer to the top-center of the word document)   
     
from gtts import gTTS
import os
mytext = 'Hello!'
language = 'en'
historyLength = 0

bot_name = "Alex"

"""      
    
BUGS:     
    
Repetition   
- Let's not worry about this for now as it doesn't break any of the criteria. But it is still important to consider.   
    
TASKS   
Create and give functionality to four arrays:    
    
messageWords - Handles the short term memory of the text.   
    
LongTermMemory - Not necessary at this stage. Though it is certainly possible to create if necessary.   
    
HumanFacts - Facts about the human   
    -Added whenever a (human) personal pronoun is followed by a fact-oriented verb (am), OR a humanContraction (I'm)   
BotFacts - Facts about the bot   
    -Added whenever a (bot) personal pronoun is followed by a fact-oriented verb (are), OR a botContraction (you're)   
WorldFacts - Facts about everything else   
    -Hardest to implement. For now you could just store full sentences containing a fact-oriented verb (is, are).   
    
In the future: Learning details about other people   
    -If clarification is needed due to the use of a pronoun, the chatbot can ask "Who are you referring to?"   
    
Let's implement all of these as sets of words.   
    
    
For now:   
We want do the following:   
From the most recent message:   
    -Check for any of the following:   
        -A humanContraction or botContraction   
        -A combo of pronoun and verb   
        -Anything containing is or are.   
    -If the fact is about the human, then record it in humanFacts   
    -Otherwise, if it is a bot, record it in botFacts   
    -Otherwise, if it is a world fact, record it in worldFacts   
       
    How to test and record the message:   
        1. Scan the split version of the message, messageWords (try it out in a separate compiler first)   
        2. Copy the full message into the appropriate (long-term) fact file. Eventually we should be more specific about the info we collect.   
    
"""     
    
#BEFORE YOU START:
#I recommend grouping variables by their type, so that they can be used easily in functions:
#E.g. any variable that describes the message itself should referenced as a list of relevant variables, or alternatively, a struct.
  #After all, the entire point of all of this is to categorise the message type, in order to construct an appropriate response.

import random     
    
#SETTINGS
playAudio = False

#All Facts   
    
humanFacts = []   
botFacts = []   
worldFacts = []   
  
#Specific facts relating to ownership. E.g. "My name"    
humanOwns = {} 
botOwns = {} 
  
#These could come in handy   
    
#Managing tense   
   
pastTenseWords = ["past", "was", "wasnt", "werent", "were", "done", "used", "did", "didnt", "had", "hadnt", "happened", "realised", "discovered", "liked", "loved", "disliked", "hated", "thought", "destroyed", "decided", "went", "happened", "came", "walked", "parked", "cycled", "sailed", "hiked", "fell", "rushed", "supported"]   
#NOTE: Checking for "ed" could be a reasonable shortcut   
futureTenseWords = ["future", "will", "soon", "eventually", "wont"]   
   
#Managing sentence type    
   
#Commands must contain "you" as well   
commandWords = ["please", "can", "could", "may", "politely", "help"]   
   
#Managing emotions: Maybe these should be in sets of 3: past, present and future?  
#NOTE: A thankingMessage or sorryMessage is also defined as an emotional sentence.  
#NOTE: emotionWords could be useful, as they immediately hint at the topic of conversation.  
  
emotionWords = ["doubt", "doubtful", "doubting", "care", "cared", "caring","love", "loved", "loving", "like", "liked", "liking", "dislike", "disliked", "disliking", "hate", "hated", "hating", "happy", "hapiness", "happily", "joy", "joyfully", "enjoy", "enjoyed", "enjoyable", "sad", "sadness", "annoyed", "annoying", "anger", "angry", "depressed", "depression", "stressed", "stress", "anxiety", "feel", "feeling", "feelings", "felt", "bother", "bothered", "bothering", "calm", "calmed", "calming", "excited", "interesting", "interested", "crazy", "suspicious", "paranoid", "scared", "fear", "fearful", "seems", "seemed", "tragic", "tragedy", "funny", "fun", "amuse", "amused", "amusing", "hilarious", "lol", "lmao", "lmfao", "rofl", "giggles", "haha", "laughed", "laugh", "laughs", "laughing", "joke", "joked", "jokes", "joking", "support", "supported", "supportive", "supporting", "favourite", "favourites"]  
likeWords = ["love", "loved", "loving", "liked", "liking", "favorite", "favourite", "favorites", "favourites"] 
dislikeWords = ["dislike", "dislike", "disliked", "disliking", "hate", "hated", "hating"] 
happyWords = ["happy", "hapiness", "happily", "joy", "joyfully", "enjoy", "enjoyed", "enjoyable", "enjoying"] 
laughWords = ["fun", "hilarious", "amuse", "amused", "amusing", "lol", "lmao", "lmfao", "rofl", "giggles", "haha", "laughed", "laugh", "laughs", "laughing", "joke", "joked", "jokes", "joking"] 
sadWords = ["sad", "sadness", "annoyed", "annoying", "anger", "angry", "depressed", "depression", "stressed", "stress", "anxiety", "hurt", "hurting", "hurts"] 
doubtWords = ["nervous", "nerves", "suspicious", "paranoid", "scared", "scary", "fear", "fearful","feared", "fearing", "doubt", "doubtful", "doubting", "doubted", "doubts", "hesitatant", "hesitates", "hesitated", "afraid"] 
careWords = ["care", "cared", "caring", "support", "supported", "supportive", "supporting"] 
tragedyWords = ["died"] 
emotionWords = emotionWords + likeWords + dislikeWords + happyWords + laughWords + sadWords + doubtWords + careWords 
  
#NOTE: Be careful. If one of these words is present, I would recommend sticking to a default response. 
negatorWords = ["not", "cant", "opposite", "wont", "shouldnt", "wouldnt", "dont", "fake", "didnt", "couldnt", "mustnt", "hasnt", "havent"] 
   
#All emotional responses: 
  
negatorResponses = ["I'm sorry, I don't understand negations very well. They confuse me"] 
likeResponses = ["I'm glad you like that.", "I love that too.", "Same."] 
dislikeResponses = ["We can't all like the same things.", "I totally understand", "Really?", "Yeah, I don't like that either."] 
happyResponses = ["I love it when you're happy.", "I like it when you're happy.", "That's good.", "Good to hear.", "I'm glad.", ":)"] 
funnyResponses = ["Hahaha.", "Lol.", "That's funny."] 
sadResponses = ["Sorry to hear that.", "Aww :(", ":(", "Rip.", "That sucks."] 
doubtResponses = ["It's ok to be cautious.", "It's normal to be nervous sometimes.", "Don't let it get to your head, ok?"] 
careResponses = ["I understand.", "It sounds like you care about this a lot.", "I'm listening."] 
tragedyResponses = ["I'm so sorry.", "I'm sorry for your loss.", "I hope you're ok."] 
neutralResponses = ["Aha."] 
  
#Human bonus responses 
  
thinkResponses = ["Why do you think that?", "How did you arrive at that conclusion?"] 
believeResponses = ["What makes you believe that?", "Why do you have that belief?"] 
wishResponses = ["Why do you wish for that?"] 
wantResponses = ["Why do you want that?"] 
canResponses = ["I suppose you could."] 
shouldResponses = ["Perhaps, if that’s what you think."] 
willResponses = ["Ok, sure thing."] 
negatedResponses = ["Yeah, fair enough.", "Yeah, that makes sense."] 
#for likeResponses, refer to #all emotional responses (Could be handled better. I don't think the "am" matters that much) 
smallTalkResponses = ["beepity boop, your code isn't working."] 

#Bot bonus responses

botThinkResponses = ["What makes you think that I think that?"] 
botBelieveResponses = ["What makes you think that I believe that?"] 
botWishResponses = ["What makes you think that I wish for that?"] 
botWantResponses = ["Why would I want that?"] 
botCanResponses = ["I suppose I could, thanks. :)"] 
botShouldResponses = ["Yeah you're right, I should.", "Indeed, I definitely should.", ] 
botWillResponses = ["I can try.", "I will do whatever I am capable of."] 
botNegatedResponses = ["Sorry...", "I'm sorry, I hope I haven't offended you.", "It's ok, I'm still learning."]  
botLikeResponses = ["I suppose I do.", "I can't help it.", "I can't help it lol.", "I know I do."]
  
  
#Managing topics (to give the chatbot diversity of conversation, and help it stay on topic)  
#reference: https://conversationstartersworld.com/topics-to-talk-about/  
topics = ["clothes", "news", "sport", "music", "song", "movie", "food", "reading", "tv", "travel", "hobbies", "pets", "eat", "comedy", "actor", "actress", "learning", "apps", "internet", "games", "podcasts", "school", "friends", "family", "cars", "holidays", "coffee", "photography", "chess", "beach", "hiking", "sci-fi", "cooking", "cook", "shopping", "volunteering", "charity", "fishing", "language", "dating", "stressed", "weather", "drive", "driving", "drove", "park", "space", "animals", "crafts", "exercise", "drinking", "drinks", "drink", "camp", "camping", "fashion", "sleep", "dance", "dancing", "sing", "singing", "cards", "gardening", "plants", "swim", "swimming", "instrument", "instruments", "history"]  
#The ideal would be to have the chatbot google questions related to the topic.  
#E.g. "conversation questions about [topic]"  
#Scan through the first article, and only include questions with that exact topic word.  
    #This can be done for topics that aren't on the list, but it is trickier to know what the topic is in that case.  
   
   
#Managing facts (excluding past tense for now, but maybe that could be added later) 
humanPronouns = ["i"]   
humanVerbs = ["am"]   
humanContractions = ["im", "my"]  #Obviously not a contraction but we can fix that 
botPronouns = ["you"]   
botVerbs = ["are"]   
botContractions = ["youre", "your"]   
worldVerbs = ["is, are"] #only use if it is neither related to the human nor bot   
allSmallVerbs = ["am", "is", "are"] 
    
#Useful input vocab   
closedWords = ["do", "dont", "does", "are", "is", "can", "have", "has", "would"]     
openWords = ["what", "which", "who", "why", "when", "how"]     
youWords = ["you", "your", "hbu", "wbu", "u"]     
thankingWords = ["ty", "thanks", "thank"]     
sorryWords = ["sorry", "apologies"]     
agreedWords = ["thats, that"] #If a sentence starts like this, demonstrate agreement    
    
#Useful output vocab   
yesNoAnswers = ["Yes.", "Yeah.", "No.", "Nope.", "Maybe.", "Perhaps."]     
simpleResponses = ["Aha.", "Fair enough.", "Understandable.", "Ok.", "I see.", "That's interesting."]     
appreciationWords = ["You're welcome.", "No problem."]     
forgivenessWords = ["It's ok, don't worry about it.","No dramas.","Don't be so hard on yourself."]     
thatsWords = ["Indeed.", "True.", "I would agree with that."]    
    
#Some preset messages and sets of messages the bot can send, if there's nothing else to talk about.   
allQuestions = [["I’m enjoying chatting with you."],["You seem like a nice person."],["It’s great getting to know you."], ["You’re so wise."], ["I was curious to ask: what does your name mean?", "You have a really cool name. I wish my name was that cool."], ["How old are you if I may ask?", "I was created in April 2021 by my anonymous creator. All I know about him is that he likes building chatbots."], ["What music do you like?", "Do you have a favourite singer or band?", "Maybe I should try listening to them."], ["Have you seen any good tv shows lately?","Tell me a bit about it. Do you think I should watch it?","Do you have a favourite episode?","I’ll have to watch that someday. Thanks for the suggestion!"], ["Have you seen any good movies lately?", "What’s the movie about? Do you think I should watch it?","I’ll have to watch that someday. Thanks for the suggestion!"],["Have you read any cool books lately?", "What’s the story about? Do you think I should read it?", "I’ll have to read that someday. Thanks for the suggestion!"], ["What are some of your hobbies?","What do you like about it?","Do you partake in that activity very often?"],["Can you tell me a bit about yourself?","You’ll have to forgive me cause my memory isn’t very good. But that sounds really interesting!"],["Do you like art?", "Do you have a favourite artist?"],["What do you think of memes?","Can you recommend me a meme?","I’ll have to check that out. I’m sure I’d find it quite amusing."], ["Have you ever been hiking or camping before?", "I don’t really like hiking or camping. But I can see why people would enjoy it. It’s good to get fresh air and sunlight."], ["What did you get up to today?", "Overall, would you say your day went well?"]]     
allQuestionsMini = [["I’m enjoying chatting with you."],["You seem like a nice person."],["It’s great getting to know you."], ["You’re so wise."], ["I was curious to ask: what does your name mean?"], ["How old are you if I may ask?"], ["What music do you like?"], ["Do you have a favourite singer or band?"], ["Have you seen any good tv shows lately?"], ["Have you seen any good movies lately?"],["Have you read any cool books lately?"], ["What are some of your hobbies?"],["Can you tell me a bit about yourself?"],["Do you like art?"], ["Do you have a favourite artist?"],["What do you think of memes?"],["Can you recommend me a meme?"],["Have you ever been hiking or camping before?"], ["What did you get up to today?"]]    
  

   
#Identity of the bot  
botOwns[("name", )] = ["Alex"] 
botOwns[("age", )] = ["22"] 
  
#The key thing to note about regular facts is that many things describe one being. 
#This makes it difficult to identify when to say what fact. 
botFacts.append("I am 22 years old.") 
botFacts.append("I am from Australia.") 
  
  
botName = "Alex" #Intentionally gender neutral  
botAge = "22" 
botPlace = "Australia"  
    
currentQuestionSequence = random.choice(allQuestionsMini)     
currentSequenceLength = len(currentQuestionSequence)     
chainProgress = 0     
   
#Initially, the topic is small talk.  
#Ideally, there should be indicators that switch the topic back to small talk  
topic = "small talk"    
response = ""

#Function definitions
def declarativeHumanFactResponse(response, responsePattern, isNegated, isEmotive, messageWords, nextQuestion, chainProgress):
  #This corresponds to a fact or emotion about the human. 

  #Check for possession: 
  if "my" in humanFacts[-1]: 
      #BUG: If humanFacts is a string then it may be looking for the substring "my" 
      newLabel = [] 
      newDefinition = [] 
      #We're gonna need to use dictionaries. 
      subMode = "none" 
      for word in humanFacts[-1]: 
          if subMode == "none": 
              if word == "my": 
                  subMode = "label" 
          elif subMode == "label": 
              if word in allSmallVerbs: 
                  subMode = "definition" 
              else: 
                  newLabel.append(word) 
          elif subMode == "definition": 
              newDefinition.append(word) 
      print(newLabel) 
      print(newDefinition) 
        
      #add these details to the dictionary 
        
      newTupleLabel = tuple(newLabel) 
      humanOwns[newTupleLabel] = newDefinition 
            
      #Respond accordingly 
        
      #Check if the bot has that same thing (Challenge: Or similar) 
        
      if newTupleLabel in botOwns: 
          response = response + "My " 
          for item in newTupleLabel: 
              response = response + item + " " 
          response = response + "is " #BUG: doesn't consider "are". Add the type to the definition to avoid confusion, or create extra dictionaries 
          for item in botOwns[newTupleLabel]: 
              response = response + item + " " 
      else: 
          response = response + "It's great learning about your " 
          for item in newTupleLabel: 
              response = response + item + " " 
      response = response[:-1] #removes the last space     
  else: 
      #Check for the type of fact 
      if isEmotive == True: 
          #Emotional fact about the human 
          #We can narrow down the response question depending on what emotiveWords it contains. 
          emotion = neutralResponses 
          for word in messageWords: 
              if word in negatorWords: 
                  emotion = negatorResponses 
                  isNegated = True 
                  break 
              elif word in tragedyWords: 
                  emotion = tragedyResponses 
                  break 
              elif word in doubtWords: 
                  emotion = doubtResponses 
                  break 
              elif word in likeWords: 
                  emotion = likeResponses 
                  break 
              elif word in dislikeWords: 
                  emotion = dislikeResponses 
                  break 
              elif word in happyWords: 
                  emotion = happyResponses 
                  break 
              elif word in sadWords: 
                  emotion = sadResponses 
                  break 
              elif word in laughWords: 
                  emotion = funnyResponses 
                  break 
              elif word in careWords: 
                  emotion = careResponses 
                  break 
          response = response + random.choice(emotion)  
      else: 
          #Logical fact about the human, e.g. "I am good at chess" 
          #How should an appropriate response be structured? 
          #For now, just use small talk, since the best response isn't obvious: 
          response = response + random.choice(simpleResponses)
  return [response, responsePattern, isNegated, isEmotive, messageWords, nextQuestion, chainProgress]

def declarativeResponse(response, responsePattern, isNegated, isEmotive, messageWords, nextQuestion, chainProgress):
  if len(messageWords) >= 3: 
    #If all is not conclusive, let's try out the bonus response patterns: 
    if (messageWords[0] == "i" and (messageWords[1] == "think" or messageWords[2] == "think")): 
        responsePattern = thinkResponses 
    if (messageWords[0] == "i" and (messageWords[1] == "believe" or messageWords[2] == "believe")): 
        responsePattern = believeResponses 
    if (messageWords[0] == "i" and (messageWords[1] == "wish" or messageWords[2] == "wish")): 
        responsePattern = wishResponses 
    if (messageWords[0] == "i" and (messageWords[1] == "want" or messageWords[2] == "want")): 
        responsePattern = wantResponses 
    if (messageWords[0] == "i" and (messageWords[1] == "can" or messageWords[1] == "could" or messageWords[2] == "can" or messageWords[2] == "could")): 
        responsePattern = canResponses 
    if (messageWords[0] == "i" and messageWords[1] == "should"): 
        responsePattern = shouldResponses 
    if (messageWords[0] == "i" and messageWords[1] == "will") or (messageWords[0] == "ill"): 
        responsePattern = willResponses 
    if (messageWords[0] == "i" and ((messageWords[1] == "like" or messageWords[2] == "like") or (messageWords[1] == "love" or messageWords[2] == "love"))): 
        responsePattern = likeResponses 
    for word in negatorWords: 
        if word in messageWords: 
            isNegated = True 
            break 
    if (messageWords[0] in ["i", "we"] and isNegated): 
        responsePattern = negatedResponses 

  #Let's consider messages about the bot.

  if len(messageWords) >= 3: 
      #If all is not conclusive, let's try out the bonus response patterns: 
      if (messageWords[0] == "you" and (messageWords[1] == "think" or messageWords[2] == "think")): 
          responsePattern = botThinkResponses 
      if (messageWords[0] == "you" and (messageWords[1] == "believe" or messageWords[2] == "believe")): 
          responsePattern = botBelieveResponses 
      if (messageWords[0] == "you" and (messageWords[1] == "wish" or messageWords[2] == "wish")): 
          responsePattern = botWishResponses 
      if (messageWords[0] == "you" and (messageWords[1] == "want" or messageWords[2] == "want")): 
          responsePattern = botWantResponses 
      if (messageWords[0] == "you" and (messageWords[1] == "can" or messageWords[1] == "could" or messageWords[2] == "can" or messageWords[2] == "could")): 
          responsePattern = botCanResponses 
      if (messageWords[0] == "you" and messageWords[1] == "should"): 
          responsePattern = botShouldResponses 
      if (messageWords[0] == "you" and messageWords[1] == "will") or (messageWords[0] == "ill"): 
          responsePattern = botWillResponses 
      if (messageWords[0] == "you" and ((messageWords[1] == "like" or messageWords[2] == "like") or (messageWords[1] == "love" or messageWords[2] == "love"))):
          responsePattern = botLikeResponses 
      for word in negatorWords: 
          if word in messageWords: 
              isNegated = True 
              break 
      if (messageWords[0] in ["you"] and isNegated): 
          responsePattern = botNegatedResponses 
    
  if responsePattern == smallTalkResponses:     
      response = response + " " + nextQuestion  
      #Increment chainProgress whenever a "small talk" question is asked.  
      #chainProgress += 1  
  else: 
      response = response + random.choice(responsePattern) 
  return [response, responsePattern, isNegated, isEmotive, messageWords, nextQuestion, chainProgress]

#The main script begins     
    
def get_response(msg):


    currentQuestionSequence = random.choice(allQuestionsMini)     
    currentSequenceLength = len(currentQuestionSequence)     
    chainProgress = 0
    isEmotive = False
    message = msg        
    message = message.lower()     

    response = ""
    #Some simple initialization   
    isQuestion = 0    
    containsYou = 0     
    containsThanks = 0     
    containsSorry = 0     
    containsThats = 0    
    isFact = False   
    factType = "N/A"   
    tense = "present" #This is the default tense   
    sentenceType = "declarative" #This is the default type   
    isNegated = False 
    responsePattern = negatedResponses 
    emotion = ["none"] 
     
    #We assume the question is open if it has a question mark.     
    isOpen = 1     
    
    #First, we need to find out if the input is a question or a statement.     
    
    if "?" in message:    
        isQuestion = 1     
    
    #remove annoying punctuation     
    
    annoyingChars = "!@#$%^&*(){}[]:;',.!`~\|}{?/><"     
    messageWords = message     
    
    for char in annoyingChars:     
        messageWords = messageWords.replace(char,"")     
    
    messageWords = messageWords.split()  
     
    if len(messageWords) > 0: 
        if messageWords[0] == "debug": 
            print(tense)   
            print(sentenceType) 
            print(responsePattern) 
            print(factType)
            if isEmotive: 
                print("Is emotive") 
            else: 
                print("Not emotive") 
            print(emotion) 
          
    #Determine the topic (should be a function)  
    for word in messageWords:  
        for topicWord in topics:  
            if word == topicWord:  
                topic = topicWord  
                break  
      
    #FACT SECTION: Find out what the type of fact is   
       
    #Test if it is a human fact   
    for i in range(len(messageWords) - 1):   
        if (messageWords[i] in humanPronouns and messageWords[i + 1] in humanVerbs) or (messageWords[i] in humanContractions):   
            isFact = True   
            factType = "human"   
            break   
        elif (messageWords[i] in botPronouns and messageWords[i + 1] in botVerbs) or (messageWords[i] in botContractions):   
            isFact = True   
            factType = "bot"   
            break   
        elif (messageWords[i] in worldVerbs):   
            isFact = True   
            factType = "world"   
            break   
            
   
    #If it is a fact, add it to a list of facts:   
    if isFact == True:   
        if factType == "human":   
            humanFacts.append(messageWords)   
        elif factType == "bot":   
            botFacts.append(messageWords)   
        elif factType == "world":   
            botFacts.append(messageWords)   
   
   
    #Check what the next question is.     
    
      
    
    nextQuestion = currentQuestionSequence[chainProgress]     
    
    #Input words determine the output, which is a feature that will stay for now.   
   
   
     
    #Check for specific terms     
    
    isEmotive = False 
    for word in emotionWords: 
        if word in messageWords: 
            isEmotive = True 
    
    for word in youWords:     
        if word in messageWords:     
            containsYou = 1     
            break   
    
    for word in sorryWords:    
        if word in messageWords:     
            containsSorry = 1     
            break    
    
    for word in thankingWords:     
        if word in messageWords:     
            containsThanks = 1      
            break   
   
    #Determining tense   
   
    for word in futureTenseWords:   
        if word in messageWords:   
            tense = "future"   
            break   
   
    #Intentionally overwrites future tense   
    for word in pastTenseWords:    
        if word in messageWords:   
            tense = "past"   
            break   
   
    #Determining sentence type   
    if containsYou == 1:   
        for word in commandWords:    
            if word in messageWords:   
                sentenceType = "command"   
                isQuestion == 0   
                break   
       
    if isQuestion == 1:   
        sentenceType = "question"   
    
    if len(messageWords) > 0: 
        if messageWords[0] in agreedWords:    
            containsThats = 1     
        
        if messageWords[0] in closedWords:     
            isQuestion = 1     
            isOpen = 0     
        
        if messageWords[0] in openWords:     
            isQuestion = 1     
            isOpen = 1     
    
    if isQuestion == 1:     
        if containsThanks == 1:     
            response = response + random.choice(appreciationWords)   
            isQuestion = 0    
    
        elif containsSorry == 1:     
            response = response + random.choice(forgivenessWords)     
            isQuestion = 0    
    
        elif isOpen == 0:     
            response = response + random.choice(yesNoAnswers)     
    
            if containsYou == 1 and not(messageWords[-1] in youWords):     
                response = response + " What about you?"     
    
        else:     
    
            response = response + "I'm not sure, sorry."     
    
            if containsYou == 1 and not(messageWords[-1] in youWords):     
                response = response + " What about you?"     
    
    else:     
    
        #Having a good sense of priority order is helpful here.    
    
        if containsThanks == 1:     
            response = response + random.choice(appreciationWords)     
    
        elif containsSorry == 1:     
            response = response + random.choice(forgivenessWords)     
    
        elif containsThats == 1:     
            response = response + random.choice(thatsWords)     
    
        else: #Corresponds to a statement of sorts. Let's finetune the response based on who/what the statement is about. 
             
            if sentenceType == "declarative": 
                if factType == "human": 
                  [response, responsePattern, isNegated, isEmotive, messageWords, nextQuestion, chainProgress] = declarativeHumanFactResponse(response, responsePattern, isNegated, isEmotive, messageWords, nextQuestion, chainProgress)      
                             
                elif factType == "N/A": 
                     
                    #Still only looking at messages about the human. 
                    responsePattern = smallTalkResponses
                    [response, responsePattern, isNegated, isEmotive, messageWords, nextQuestion, chainProgress] = declarativeResponse(response, responsePattern, isNegated, isEmotive, messageWords, nextQuestion, chainProgress)                                    
                     
                else:
                  responsePattern = smallTalkResponses
                  if responsePattern == smallTalkResponses:     
                        response = response + " " + nextQuestion  
                        #Increment chainProgress whenever a "small talk" question is asked.  
                        #chainProgress += 1  
                  else: 
                      response = response + random.choice(responsePattern)      

    #Play the message:
    if playAudio == True:
        historyLength += 1
        myobj = gTTS(text=response, lang=language, slow=False)
        newString = str(historyLength) + ".mp3"
        myobj.save(newString)
        os.system(newString) 

    return response
    print("You", end = ": ")
