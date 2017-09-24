# Welcome to UnbelievaBoat
<a href="https://discordapp.com/oauth2/authorize?permissions=268561414&scope=bot&client_id=292953664492929025" rel="some text">![Invite 🍕 UnbelievaBoat 🍕](http://unbelievable-bot.readthedocs.io/en/latest/img/inviteBot.png)</a>
<a href="https://discord.gg/YMJ2dGp" rel="some text">![Join Server](http://unbelievable-bot.readthedocs.io/en/latest/img/joinServer.png)</a>


## So, what does this bot do?
- Moderation (yep, like all other bots *¯\\_(ツ)\_/¯*)
- Money (each server has it's own economy)
- Casino / Gambling Games
- Earn money from chatting
- Tribes (Raids!)
- Other stuff that I've forgotten about

## How to Earn Money?
1. Contribute to chat in text channels (if it's been enabled in that channel) -> This doesn't mean spam!
2. Play Games -> See below for game commands.
3. Be a slut... Use the command `slut` to get some quick dirty cash.
4. If being a slut isn't your thing, you can work <u>instead</u> using the command `work`.
5. If you're feeling more risky, you can commit a crime <u>instead</u> using the command `crime`. This has a higher risk of failing, but also a higher payout.
6. Deposit money to the bank to earn interest and keep it safe. See the current interest rate using `bank`.

## What to do with Money Earned?
1. Use it as bets for games to earn even more money.
2. Purchase something from the store
3. Give it to another member? idk
4. Show off


# Commands
All commands much be initiated with the prefix. By default this is `!`. You can also `@mention` the bot.
For example `!help` or `@UnbelievaBoat#1046  help`.

The syntax of the command usage is:  Optional parameter: `[]` Required parameter: `<>`. **DO NOT INCLUDE THESE WHEN TYPING THE COMMAND**

`member` means an `@mention` or typing the member's name. Both `@UnbelievaBoat#1046` and `Unbelievable Bot` are valid `member`.

**Some commands can only be used by  `Server Admin`, `Mod Role` or `Bot Commander`.** Note: Server Admin also has Mod Role & Bot Commander permissions.


#### Utility
Any abuse of the request commands will = blacklist tbh. Ain't nobody got time for dat.

| Command           | Description                                                                                       | Usage                         |
| ----------------- | ------------------------------------------------------------------------------------------------- | ----------------------------- |
| `help`            | Get a link to this page and the support/official server                                           | `help`
| `prefix`          | Shows or sets the command prefix. **`Server Admin`** required to set prefix                       | `prefix [prefix]`
| `invite`          | Gives you an invite link to add this bot to your server                                           | `invite`
| `donate`          | If you're enjoying the bot, and would like to donate. This gives you the PayPal and Patreon link  | `donate`
|                   | <br>                                                                                              |
| `request-feature` | Request a feature you'd like adding. This command can only can be used in official server.        | `request-feature <feature description>`



#### Setup
Setup UnbelievaBoat for your server, all settings are, by default, **disabled**.

| Command                   | Description                                                                                               | Usage                             |
| ------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------- |
| `create-muted-role`       | Creates the muted role for use with the `mute` command **`Mod Role`**                                     | `create-muted-role`
| `set-muted-role`          | Uses an already created muted role for the `mute` command **`Mod Role`**                                  | `set-muted-role <role>`
| `view-setup`              | Used view the current setup of the bot on your server                                                     | `view-setup`
|                           | <br>                                                                                                      |
| `enable-agree`            | Require new members to type `agree` in the welcome/guest channel **`Server Admin`**                       | `enable-agree <channel> [message]`
| `enable-bot-commander`    | Set the role that can use `Bot Commander` commands **`Server Admin`**                                     | `enable-bot-commander <role>`
| `enable-log-channel`      | Set the channel to keep a history of mod moderation actions like `kick`, `ban`  **`Server Admin`**        | `enable-log-channel <channel>`
| `enable-mod-role`         | Set the role that can use `Mod Role` commands **`Server Admin`**                                          | `enable-mod-role <role>`
| `enable-welcome`          | Add a welcome message to send when a new member joins **`Server Admin`**<br>Tags: `{user}` `{server}`     | `enable-welcome <channel> <message>`
| `enable-leave-message`    | Add a leave message to send when a member leaves **`Server Admin`**<br>Tags: `{user}` `{server}`          | `enable-leave-message <channel> <message>`
| `enable-whats-new`        | With this enabled, any announcements on new features will go straight to your server. **`Server Admin`**  | `enable-whats-new <channel>`
|                           | <br>                                                                                                      |
| `disable-agree`           | No longer require new members to type `agree` in the welcome/guest channel **`Server Admin`**             | `agree-disable`
| `disable-chatbot`         | Disables chatting with the bot **`Server Admin`**                                                         | `disable-chatbot`
| `disable-bot-commander`   | Disables `Bot Commander` only commands being used by this role **`Server Admin`**                         | `disable-bot-commander`
| `disable-log-channel`     | Disables logging mod actions, this doesn't delete the actual channel **`Server Admin`**                   | `disable-log-channel`
| `disable-mod-role`        | Disables `Mod Role` only commands being used by this role. **`Server Admin`**                             | `disable-mod-role`
| `disable-welcome`         | Disables the welcome message for when a user joins **`Server Admin`**                                     | `disable-welcome`
| `disable-leave-message`   | Disables the leave message for when a user leaves **`Server Admin`**                                      | `disable-leave-message`
| `disable-whats-new`       | Disables announcements to the channel **`Server Admin`**                                                  | `disable-whats-new`



#### Economy
All things money related. Channels are **locked** by default.

| Command               | Description                                                                                    | Usage                         |
| --------------------- | ---------------------------------------------------------------------------------------------- | ----------------------------- |
| `bank`                | Displays how much **The Bank** has and the current interest rate                               | `bank`
| `money`               | Displays the money you, or another member, have earned                                         | `money [member]`
| `slut`                | Whip it out to earn extra money 🍆   *(cool-down)*                                             | `slut`
| `work`                | Instead of whipping it out, you can work instead   *(cool-down)*                               | `work`
| `crime`               | Commit a crime 👀 This has a higher payout, but also higher risk of failing   *(cool-down)*    | `crime`
| `deposit`             | Deposit money to the bank                                                                      | `deposit <amount or -all>`
| `withdraw`            | Withdraw your money from the bank                                                              | `withdraw <amount or -all>`
| `leaderboard`         | Displays the richest in your server.                                                           | `leaderboard`
| `give-money`          | Give your money to another member.                                                             | `give-money <member> <amount or -all>`
|                       | <br>                                                                                           |
| `add-money`           | Add money to a member's cash **`Bot Commander`**                                               | `add-money <member> <amount>`
| `remove-money`        | Remove money from a member's cash **`Bot Commander`**                                          | `remove-money <member> <amount>`
| `set-interest-rate`   | Set the interest rate of the bank (between 0 - 15) **`Bot Commander`**                         | `set-interest-rate <rate>`
| `set-cooldown`        | Set the cooldown between using slut/work/crime commands **`Bot Commander`**                    | `set-cooldown <hours>`
| `set-currency`        | Change the currency symbol to any set of characters you want (e.g. `set-currency unbelievable bot`) **`Bot Commander`**            | `set-currency <new currency>`
| `lock`                | Disable money earning from chatting in a channel **`Bot Commander`**                           | `lock [channel]`
| `lock-all`            | Disable money earning from chatting on all channels in the server **`Bot Commander`**          | `lock-all`
| `unlock`              | Enable money earning from chatting in a channel **`Bot Commander`**                            | `unlock [channel]`
| `reset-economy`       | Pretty much what it sounds like. USE WITH CAUTION **`Server Admin`**                           | `reset-economy`



#### Games

| Command               | Description                                                                   | Usage                         |
| --------------------- | ----------------------------------------------------------------------------- | ----------------------------- |
| `blackjack`           | Play a game of blackjack for money <br>*(1 Player)*                           | `blackjack <bet>`
| `roulette-info`       | Displays information about the roulette                                       | `roulette-info`
| `roulette`            | Play a game of roulette for money <br>*(1+ Players)*                          | `roulette <bet> <space>`
| `russian-roulette`    | Play a game of Russian roulette for money <br>*(2-6 Players)*                 | `russian-roulette`
| `slot-machine`        | Play a round with the slot machine with coins purchased <br>*(1 Player)*      | `slot-machine <NÂº of coins>`
| `cock-fight`          | Place your bets and send your chicken off to fight <br>*(1 Player)*           | `cock-fight <bet>`
| `greyhound-race`      | Bet & pick which greyhound you think will win the race <br>*(1+ Players)*     | `greyhound-race <bet> <greyhound #>`
|                       | <br>                                                                          |
| `set-game-cooldown`   | Set the how many times a game can be played in x seconds **`Bot Commander`**  | `set-game-cooldown <usages> <duration>`



#### Tribes
A tribe gives you your very own private text channel and role to chat with fellow tribe members.<br>

| Command           | Description                                                                                                   | Usage                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| `create-tribe`    | Create your own tribe! e.g `create-tribe 'unbelievable peeps' pink`                                           | `create-tribe <tribe name> [colour or #hex]`
| `join-tribe`      | Join an existing tribe, you can only be in one tribe per servers                                            | `join-tribe <tribe name>`
| `leave-tribe`     | Leave the tribe you're in                                                                                     | `leave-tribe`
| `list-tribes`     | Display a list of all tribes in the server                                                                    | `list-tribes`
| `tribe-bank`      | View the balance of the tribe bank                                                                            | `tribe-bank`
| `tribe-deposit`   | Deposit your money to the tribe bank                                                                          | `tribe-deposit <amount>`
| `tribe-store`     | View the weapons and armour you can buy for your tribe                                                        | `tribe-store [page]`
| `tribe-inventory` | View the weapons and armour your tribe has                                                                    | `tribe-inventory [page]`
|                   | <br>                                                                                                          |
| `tribe-kick`      | Kick a member from your tribe **`Tribe Owner`** or **`Server Admin`**                                         | `tribe-kick <member>`
| `tribe-ban`       | Ban a member from your tribe (Currently no unban so use with caution) **`Tribe Owner`** or **`Server Admin`** | `tribe-ban <member>`
| `rename-tribe`    | Rename your tribe (must be done in tribe channel) **`Tribe Owner`** or **`Server Admin`**                     | `rename-tribe <new name>`
| `delete-tribe`    | The tribe creator can delete their tribe. <br>This removes all tribe members, the role and the text channel | `delete-tribe <tribe name>`
|                   | <br>
| `set-tribe-cost`  | Set how much tribes cost for members to create in your server **`Server Admin`**                              | `set-tribe-cost <amount>`
| `set-tribe-income`| Set the amount you want tribes members on your server to get every 12 hours **`Server Admin`**                | `set-tribe-income <amount>`
| `create-weapon`   | Create a weapon for tribe owners to buy for tribe raids **`Server Admin`**                                    | `create-weapon`
| `create-armour`   | Create armour for tribe owners to buy to protect you for tribe raids **`Server Admin`**                       | `create-armour`
| `remove-weapon`   | Delete a weapon from the tribe store **`Server Admin`**                                                       | `remove-weapon <name>`
| `remove-armour`   | Delete armour from the tribe store **`Server Admin`**                                                         | `remove-armour <name>`
| `tribe-raid`      | Raid another tribe on your server, the success of the raid is calculated using the equipment and number of members both tribes have | `tribe-raid <tribe name>`



#### Info

| Command           | Description                                                           | Usage                             |
| ----------------- | --------------------------------------------------------------------- | --------------------------------- |
| `view-blacklist`  | View users on the blacklist (use argument `-g` for global blacklist)  | `view-blacklist [global argument]`
| `view-case`       | View details on a case                                                | `view-case <case id>`
| `profile`         | Displays your profile, or the profile of any user                     | `profile [member]`
| `server-info`      | View statistics about your server.                                   | `server-info`
| `stats`           | Displays some statistics about unbelievable bot                       | `stats`
| `punishments`     | View your, or another user's punishments                              | `punishments [member]`



#### Items

| Command           | Description                                                               | Usage                                        |
| ----------------- | ------------------------------------------------------------------------- | -------------------------------------------- |
| `buy`             | Buys an item at the store (put the name in quotes if more than 1 word)    | `buy-item <'item name'> [amount to buy]`
| `item-info`       | Displays more details on an item                                          | `item-info <item name>`
| `inventory`       | Displays the items you have in your inventory                             | `inventory <page> [member]`
| `store`           | Displays the price of all items                                           | `store [page]`
| `server-store`    | Displays items that are just for your server                              | `server-store [page]`
| `use-item`        | Removes 1 of the named item from your inventory                           | `use <item name>`
| `use-item-all`    | Removes all of the named item from your inventory                         | `use-item-all <item name>`
| `sell-item`       | Sell your items to another member (5 mins to accept)                      | `sell-item <member> <'item name'> <amount> <price>`
|                   | <br>                                                                      |
| `create-item`     | Add a new item to your server store **`Bot Commander`**                   | `create-item`
| `remove-item`     | Removes an item from your server store **`Bot Commander`**                | `remove-item <name>`


#### Moderation **`Mod Role`**
Used to moderate your server.<br>
(This will be updated accordingly when Discord Audit Logs ~~are released~~ can be tracked)

| Command           | Description                                                                                               | Usage                                         |
| ----------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------- |
| `ban`             | Bans a member from the server                                                                             | `ban <member> <reason>`
| `blacklist-add`   | Prohibit a user from using unbelievable bot commands in your server                                       | `blacklist-add <member>`
| `blacklist-remove`| Remove a user from the command blacklist                                                                  | `blacklist-remove <member>`
| `launch-cybernuke`| Bans all members that have joined recently, with new accounts **`Server Admin`**                          | `launch-cybernuke <member age> <account age>`
| `kick`            | Kicks a member from the server                                                                            | `kick <member> <reason>`
| `mute`            | Mutes a member from the server (prevents sending messages and speaking in voice)                          | `mute <member> <length in hours> <reason>`
| `purge`           | Deletes messages. Limit is capped at 100.                                                                 | `purge [limit] [member, -users or -bots]`
| `rm-punish`       | Removes a punishment [mute / warn / kick / ban] from the database.                                        | `rm-punish <case id> [reason]`
| `unmute`          | Un-mutes a member from the server (allows sending messages and speaking in voice)                         | `unmute <member> [reason]`
| `warn`            | Gives member a warning for breaking the rules                                                             | `warn <member> <reason>`



#### Weather
Wanna know what the weather is somewhere?

| Command           | Description                                                       | Usage                         |
| ----------------- | ----------------------------------------------------------------- | ----------------------------- |
| `weather`         | Get the weather                                                   | `weather <location>`



#### Command Selection
Any command or group of commands can be disabled using `enable` or `disable`.

| Command           | Description                                                       | Usage                         |
| ----------------- | ----------------------------------------------------------------- | ----------------------------- |
| `groups`          | List all command groups                                           | `groups`
| `enable`          | Enables a command or command group **`Server Admin`**             | `enable <command/group>`
| `disable`         | Disables a command or command group **`Server Admin`**            | `disable <command/group>`