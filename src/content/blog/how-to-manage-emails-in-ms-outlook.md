---
title: "How to manage emails in MS Outlook"
date: 2013-10-20T00:43:00.000+05:30
author: "Ganesh Pagade"
tags: ["tools", "productivity"]
draft: false
---

We use Outlook in our office for all the email communication. And each day I spend considerable amount of time reading and responding to mails. I have tried many different approaches to manage emails efficiently - creating folders, applying rules and filters, setting categories, setting flags, Outlook plugins and so on. Some of them have helped. But I always lagged behind the incoming rate of mails. Sometimes I ended up spending my weekend in cleaning up my inbox. Sometimes I was late to respond and sometimes even miss out on the mail completely.

Over period of time, while continuously trying new things, I have settled down to the process which has not only increased my effectiveness (like giving timely response to mails, not missing out on any mail) but also efficiency (by taking more incoming rate of mails by subscribing to more mailing-lists and contributing to the discussions).

In this post I'll try to describe the process that has worked for me. First I'll talk about all the settings that I have done in my Outlook and then I'll describe the process or flow that I follow for every mail using those settings.

# 1. The Settings

## 1.1. Keep mails unread unless you explicitly mark them read

To be in control of your mails, you should be explicitly marking the mails as read when they are really read. Letting Outlook do it for you is recipe for missing out on mails. I figured this out the hard way.

So first thing is to change the Outlook settings. To do this in Outlook 2010, go to View -> Reading Pane (in Layout) -> Options. Following window should pop up. Unselect first two check boxes.

![](/images/posts/2013-10-20-how-to-manage-emails-in-ms-outlook/KeepRead.png)

These two check boxes, if checked, marks the mail as read automatically. This caused my mails getting marked as read even when I had no intention to do so. This resulted in missing out on important mails and action items. I had to explicitly mark a mail as unread, if I wanted to revisit it again and that was error prone and not so convenient.

Now that all mails will remain unread as long as we don't explicitly mark them read, here's a simple rule to follow: A mail will remain unread as long as there is an action item pending on it. An action item can be: just reading the mail again, actually performing some action and/or replying the mail, waiting for some event to happen etc.

## 1.2. Get rid of all the folders

'Folders' is more work. You have to go to every folder to check mails. And if the folder contains not-so-important-mails (mails from some forum you would like to contribute), you might just not check mails in that folder.

Also if folder already contains unread mails, its difficult to know if new mail has arrived unless you remember previous unread mails' count or you actually go to that folder.

I had rules which would put incoming mails to folders based on various criterion. Most of the time I simply forgot to check mails in these folders. I only went to them occasionally to delete all the mails and clean them up.

I had many such folders and they were kind of hiding the mails from me.

Now all my mails either go to my Inbox folder or directly go to Deleted Items folder. That's it - just one more location to look for mails other than the Inbox. And it is pre-created.

Note that even though a mail goes directly into Deleted Items folder, it is still unread, which means I still have an action item on it.

## 1.3. Create Rules to move mails to Deleted Items
Action to be performed by all your rules will be to move the mail to Deleted Items folder.

![](/images/posts/2013-10-20-how-to-manage-emails-in-ms-outlook/MoveToDeletedItems.png)

All mailing lists, auto-generated mails, alert/notification mails etc go directly into Deleted Items. For ex: daily build pass/fail mails, check-in mail alerts, test case failures, forums where people ask for help etc. should go to Deleted Items. Rest all go into Inbox. 

Again, mail remains unread at both the locations.

## 1.4. Create Categories and Search Folders

You are more likely to and comfortable to mark a mail as read when you know you will be able to find it if needed in future. So its essential to organize and categorize your mails in some way.

And the best way to organize the mails is to align them to your searching thought process. Just ask yourself: "How would I search this mail, if I needed it 1/3/6 months down the line?". Create categories based on the answer.

Think about the categories which would be most helpful when you have to a search a mail in future. Don't be shy to create as many categories as you want.

Main advantage of Categories over Folders is that you can assign multiple categories to single mail. So the same mail would be visible under multiple categories. This simply increases the chances of finding the mail.

I prefer manually assigning categories to a mail rather than setting them through some rule. This increases the precision and in turn increases the chances of finding the mail.

Also I find it useful to create categories based on work modules instead of based on sender's mail-id.

After categories, create Search Folders for each category. This keeps your mails grouped for you to search/refer in future. It kind of replaces the Folders. But you use it mainly for searching. Like a said, a single mail can have multiple categories and hence it can appear in multiple search folders. It's equivalent to 'Label' in GMail.

## 1.5. Create Quick Steps

In Outlook 2010 you can define 'Quick Steps' which performs set of actions on a mail.

![](/images/posts/2013-10-20-how-to-manage-emails-in-ms-outlook/QuickSteps.png)

Create two Quick Steps:

1. **Permanent Delete** - This permanently deletes the mail.
1. **Read & Delete** - This marks the mail as Read, Deletes the mail and send it to Deleted Items folder.

You can also assign short-cut keys to perform the Quick Steps defined.

![](/images/posts/2013-10-20-how-to-manage-emails-in-ms-outlook/ReadAndDelete.png)

## 1.6. Know your Server Settings

You should know few Server Settings applied to every mail box in your organization. For example, how long does a mail remain in Deleted Items folder before it gets permanently deleted, whats the auto-archive frequency etc.

In my case, a mail remains for 2 months before it gets permanently deleted from Deleted Items. Auto-archive happens every 2 weeks. A mail remains in Inbox for 2 months after which it is archived and moved to archive Inbox.

All this happens automatically based on archive and server settings and I don't have to worry about it.

# 2. The Process

With all these settings in place, we are now ready to handle the incoming mails.

Any incoming mail will either go into Inbox or Deleted Items.

In Inbox, after reading a mail, I:

## 2.1. Delete Permanently

When I am sure the mail is irrelevant to me and I have no action item on it today or in future and I will never need this mail again. Example: Announcement mail of some upcoming sports event you are not interested or mail threads you are unnecessarily part of. For this, I use Quick Step defined in 5.1 above. Shortcut key: Shift + Del

## 2.2. Mark Read and Delete

When there is no action item pending on me but I might need the mail for reference in near future. That near future has to be less than 2 months. So this action is for mails which would become irrelevant after few weeks and are no longer required for long term reference. The mail goes into Deleted Items and would be permanently (auto) deleted after 2 months. Example: Weekly status report/defect report sent by somebody. For this, I use Quick Step defined in 5.2 above. Shortcut key: Ctrl + q, Ctrl + d

## 2.3. Mark Read

When there is no action item pending on me but the mail contains information which I might need in future. The mail remains in Inbox. I assign category/categories to the mail so that it would be easier to find it in future. If there is some trivial action item or follow up to be done, I also assign a follow up flag with reminder. But normally I use step 4 mentioned below for followups. Example would be: Mail contains information about workaround to be used for a particular product issue. Shortcut key: Ctrl + q

## 2.4. Keep the mail unread and in Inbox

When there is an action item on me. I might have to perform some task, reply to the mail or followup on the mail in a day or two or simply re-read the mail/attachments. For all such situations I keep the mail unread. And once the action item is done, I again perform one of the above three actions on the mail. Example: Mail asking to update the ETAs for defects on my name. I wont permanently delete this mail unless I go and update the ETAs in our defect tracking system.

In Deleted Items, after reading a mail, I:

1. **Delete Permanently** - Reason same as 1 above. Shortcut key: Ctrl + d
1. **Mark Read** - Reason same as 2 above. Shortcut key: Ctrl + q
1. **Move to Inbox** - very rarely when the mail contains information or has action item on me. Once mail is moved to Inbox, follow the steps mention in above section. If you are frequently moving mails from Deleted Items to Inbox, its time to revisit your Outlook rules.

After replying to a mail, I:

1. **Mark Unread in Inbox** - Reasons same as point 4 mentioned above i.e. there is still action item pending on me. Shortcut key: Ctrl + u.
1. **Mark Unread in Sent Items** - when I am expecting a reply from someone  else on the mail I just sent and until then there is no action item on me. Shortcut key: Ctrl + u. If you don't want one more folder to track, just mark the mail as unread in Inbox.

Finally, change the view of your Inbox and Delete Items folders to view only unread mails:

![](/images/posts/2013-10-20-how-to-manage-emails-in-ms-outlook/View.png)

This will keep your focus on the mails which has some action items pending on you. You would occasionally change this view, to search for some mails or view the mails marked read. But for most of the time you would only see the unread mails present in your Inbox and Deleted Items.

# Some Parting Tips

1. The process may sound complicated but once it fits in your brain, you would perform the actions in split second.
1. Don't be afraid to delete mails. Rarely, if you need a mail that you have permanently deleted, you can always request the sender or your teammate to resend it to you.
1. When in doubt - mark the mail as read. Doubt should signify that there is no action item on you. If you can't quickly decide whether the mail will be required in future or not, just mark it read. It will come up in search, if it is required.
1. Familiarize yourself to the keyboard shortcuts and use them as far as possible.
1. Never delete any mail that you sent. That goes without saying, but still.

I hope someone finds this useful. I would love to know if you have any better way to manage mails or have any suggestions to improve above process.
