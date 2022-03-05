import discord
import datetime

class ReminderClass:
    def __init__(self, dateNow, dateToReminder, contentReminder, userID):
        self.dateNow = dateNow
        self.dateToReminder = dateToReminder
        self.contentReminder = contentReminder
        self.userID = userID
        self.subscribedUsers = []

    def __str__(self):
        return f"{self.contentReminder} at {self.dateToReminder}"

def CreateReminder(dateToReminder, contentOfReminder, userID):
    reminderToReturn = ReminderClass(datetime.datetime.now(), dateToReminder, contentOfReminder, userID)
    return reminderToReturn

#activity = discord.Activity(name='the sound of silence', type=discord.ActivityType.listening)
client = discord.Client()
TOKEN = "OTQ1ODEyMDc4NTIwODQwMTky.YhVmIw.G8792_aUBxzVkClj5q79tJdUL0Y"

toDoList = [] #Declaring an empty list which will contain the tasks
newReminder1 = CreateReminder("11/03/2022 19:22", "End of the Ukranian war", 0)
newReminder2 = CreateReminder("06/03/2022 23:59", "Kuni elindul az egyetemre", 0)
newReminder3 = CreateReminder("23/07/2000 22:22", "Beginning of a trainsurfer's life", 0)
toDoList.append(newReminder1) #These tests were created on 5th March
toDoList.append(newReminder2)
toDoList.append(newReminder3)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.invisible) #sets the bot invisible, had to use it as someone always spammed it
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    #Help
    if message.content.lower().startswith('hey kazo?'):
        await message.channel.send("You can easily manage reminders with me.")
        await message.channel.send("For commands, type 'Hey Kazo, show command list'.")

    # Help
    if message.content.lower().startswith('hey kazo, show command list'):
        await message.channel.send("Available commands:\n------------------------\nShow all reminders\nShow my reminders\nSubscribe to a reminder\nCreate a reminder\nRemove a reminder\nUpdate a reminder\nDelete all reminders and just die instead")

    #Show all reminders
    if message.content.lower().startswith('hey kazo, show all reminders'):
        toPrint = "The reminders are:\n----------------------\n"
        for x in toDoList:
            toPrint+=str(x)+"\n"
        await message.channel.send(toPrint)

    #Show my reminders
    if message.content.lower().startswith('hey kazo, show my reminders'):
        toPrint = "Reminders created by you:\n----------------------\n"
        for x in toDoList:
            if (message.author.id==x.userID):
                toPrint+=str(x)+"\n"
        await message.channel.send(toPrint)

    #Adding a reminder
    if message.content.lower().startswith('hey kazo, create a reminder'):
        await message.channel.send("Title of the reminder:")
        response = await client.wait_for("message")
        """if response.content == 'yes':
            await message.channel.send('You said yes.')
        elif response.content == 'no':
            await message.channel.send('You said no.')
        else:
            await message.channel.send("That isn't a valid response.")"""
        title = response.content
        id = response.author.id
        await message.channel.send("Deadline of the reminder (DD/MM/YYYY HH:MM):")
        timeResponse = await client.wait_for("message")
        deadline = datetime.datetime.strptime(timeResponse.content, '%d/%m/%Y %H:%M')
        newReminder = CreateReminder(deadline, title, id)
        await message.channel.send(f"A new reminder has been created: {newReminder}")
        toDoList.append(newReminder)

    #Removing a reminder
    if message.content.startswith('hey kazo, remove a reminder'):
        toPrint = "The available reminders are:\n----------------------\n"
        i = 0
        while i < len(toDoList):
            toPrint += (str(i+1)+". "+str(toDoList[i]) + "\n")
            i += 1
        #for x in toDoList:
        #    toPrint += +". "+str(x) + "\n"
        await message.channel.send(toPrint)
        await message.channel.send("Which one would you like to delete (id)?")
        response = await client.wait_for("message")
        await message.channel.send("Removed "+str(toDoList[int(response.content)-1]))
        toDoList.remove(toDoList[int(response.content)-1])

    #Modifying a reminder
    if message.content.startswith('hey kazo, update a reminder'):
        toPrint = "The available reminders are:\n----------------------\n"
        i = 0
        while i < len(toDoList):
            toPrint += (str(i + 1) + ". " + str(toDoList[i]) + "\n")
            i += 1
        # for x in toDoList:
        #    toPrint += +". "+str(x) + "\n"
        await message.channel.send(toPrint)
        await message.channel.send("Which one would you like to upgrade (id)?")
        idToUpgrade = await client.wait_for("message")
        itemToUpgrade = toDoList[int(idToUpgrade.content)-1]
        await message.channel.send("You have selected: " + str(toDoList[int(idToUpgrade.content) - 1]))
        await message.channel.send("What do you want to change (Content/Time)")
        responseToChange = await client.wait_for("message")
        for i, item in enumerate(toDoList):
            if (item == itemToUpgrade):
                if (responseToChange.content.lower()=="content"):
                    await message.channel.send("What's the new title of the reminder?")
                    toDoList[i].contentReminder = (await client.wait_for("message")).content
                    await message.channel.send(f"Reminder succesfully updated: {str(toDoList[i])}")
                elif (item == itemToUpgrade) & (responseToChange.content.lower()=="time"):
                    await message.channel.send("What's the new date/time of the reminder (DD/MM/YYYY HH:MM)?")
                    toDoList[i].dateToReminder = datetime.datetime.strptime((await client.wait_for("message")).content, '%d/%m/%Y %H:%M')
                    await message.channel.send(f"Reminder succesfully updated: {str(toDoList[i])}")
                else:
                    await message.channel.send(f"Invalid user input, try again, or type 'Hey Kazo?' to get some help")

    #Delete all reminders
    if message.content.startswith('hey kazo, delete all reminders'):
        toDoList.clear()
        await message.channel.send("Deleted all the reminders, you can die now in peace.")

    #Subscribe to a reminder
    if message.content.startswith('hey kazo, subscribe to a reminder'):
        toPrint = "The available reminders are:\n----------------------\n"
        i = 0
        while i < len(toDoList):
            toPrint += (str(i + 1) + ". " + str(toDoList[i]) + "\n")
            i += 1
        await message.channel.send(toPrint)
        await message.channel.send("Which reminder do you want to subscribe (id)?")
        idToSubscribe = await client.wait_for("message")
        (toDoList[int(idToSubscribe.content)-1].subscribedUsers).append(str(message.author.id))
        await message.channel.send(f"You successfully subscribed to {toDoList[int(idToSubscribe.content)-1]}")

    #testreminder
    if message.content.startswith('testreminder'):
        await message.channel.send("Which?")
        idTestremind = await client.wait_for("message")
        usersToPing=""
        for x in toDoList[int(idTestremind.content)-1].subscribedUsers:
            usersToPing+="<@"+str(x)+"> "
        await message.channel.send(f"{toDoList[int(idTestremind.content)-1]} {usersToPing}")


client.run(TOKEN)