# BytesToBits ModMail
> *This is the source code of our ModMail bot. If you wish to use it on your server, go ahead. If you want to copy anything to add to your own bot, you're free to do that too. This code is old, but still functional, so it is useful. Once we decide to update the ModMail bot, we will update the repo as well.*

# How to setup

## Configuring the Bot
- **Categories:** to add/remove/edit categories, you will need to edit the `data/categories.yml` file. All categories must follow this format *(except from the `Cancel` category)*
```yaml
CategoryName:
    mention: "Mention Message <@roleid>" // Message on thread creation
    category: 759762394179436554 // Thread Category ID
    description: "Category Description" // Will be shown to the recipient
    emoji: "❓" // Emoji for the user to react
```
- **Close Message:** Whenever a thread is closed, you can automate a message by editing `data/closeMessage.txt`.
- **Editing `data/config.yml`:** Just change all values to match your server settings. The main guild is the server to receive support messages from, and the support guild is the server to create the threads in. They **can** be the same guild. The support role is the only role who can reply to ModMails.

## Preparing the Database
To be able to use the bot, you need a **Mongo Database**. You can get a free **500MB** Database from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas). That will last for a really long time.

Head over to Atlas and create a new account. You will then be greeted with this panel.
![Panel View](https://user-images.githubusercontent.com/44692189/64170897-1297a600-ce73-11e9-910e-38b78c3ac315.jpg)

Select the `FREE` one and give it a name. Follow these steps;
- Go to `Database Access` section under the `Security` tab and click `+ ADD NEW USER`. Give it `Read and write to any database` permissions so the bot can properly store the data. Give it a username and a **secure** password. Save the password only.
![New User](https://i.imgur.com/zfhxyNX.png)
- To allow the bot to actually access the database, you should whitelist all IP's. Go to `Network Access` section under the `Security` tab and click `+ ADD IP ADDRESS`. Click the `Allow Access From Everywhere` and `0.0.0.0/0` should appear in the `Whitelist Entry`. If it doesn't, enter it manually. Lastly, click confirm.
![Whitelist All IP's](https://i.imgur.com/UgIYkoA.png)
- Time to connect to the Database! Go to `Cluster` under the `DATA STORAGE` tab. If your database is still setting up, please wait until it's done! Once it is, click the `CONNECT` button and `Connect Your Application`. Copy a link that **looks** like this; `mongodb+srv://<username>:<password>@cluster0.r4nd0m.mongodb.net/myFirstDatabase?retryWrites=true&w=majority`
- Lastly, remove the `myFirstDatabase?retryWrites=true&w=majority` part and replace `<username>` with your user's name (sometimes it is already replaced in if there's only one user), and `<password>` with your saved password. Take the link and paste it as the value of `mongo-uri` in `data/config.yml`!
- Your database is done!

> *That's pretty much it. I'd usually say any contributions are welcome, but it's a waste of time since this code is not going to be updated until we recreate the whole bot. Enjoy <3*