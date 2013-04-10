
webpagechecker
=============

A utility to check websites for changes, and then query the datastore for any changes that have been seen.

It maintains a datastore containing known URLs to check, and treats checking the URLs and 
telling the user about any changes as completely seperate operations.

It has a plugin model for specifying ways of determining "changes" in a website.
Some examples of detection methods are checking the E-Tag header, or hashing the contents of the page.
But in principle more specific methods could be used, such as checking a specific element.
This might help eliminate false positives if you only care about specific content.

As an example real-world use of this kind of model, you might run

	webpagechecker check URL1 URL2 URL3

to set up the list of URLs to check, then run

	webpagechecker check

as a cron job every hour.

Then you could periodically see if there have been any changes with

	webpagechecker show

or, as part of a script,

	webpagechecker query

which returns non-zero if any changes are pending. In fact, this particular form of invocation
has been optimised specifically so it can be used in a PS1 without causing noticable lag.

Once you have seen a change alert, you can clear it with

	webpagechecker clear URL

Dependencies
-----------

Some of these dependencies could be edited around - for example simplejson
could be easily replaced with the standard python JSON library.
I'm simply an opinionated person, and I suggest that if you aren't using the following,
you *should* be.

* python 2.7
* gevent >=1.0
* requests
* simplejson
