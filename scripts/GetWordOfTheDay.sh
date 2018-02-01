#!/bin/sh
exec scala -savecompiled -classpath "lib/AtomReaderLibrary-assembly-1.0.jar" "$0" "$@"
!#

import java.net.URL
import com.rometools.rome.feed.synd.{SyndContent, SyndEntry, SyndFeed}
import com.rometools.rome.io.SyndFeedInput
import com.rometools.rome.io.XmlReader
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import com.alvinalexander.atom.JsoupFormatter

// read the desired feed with ROME
val feedUrl = new URL("https://www.merriam-webster.com/wotd/feed/rss2")
val input = new SyndFeedInput
val feed: SyndFeed = input.build(new XmlReader(feedUrl))

// convert it to a Scala `Seq`
import scala.collection.JavaConverters._
val entries: Seq[SyndEntry] = asScalaBuffer(feed.getEntries).toVector

// get the first entry (today’s word of the day)
val entry = entries(0)

// the title is the word of the day
println("")
println("Word of the Day")
println("---------------")
println("")
println(s"Word: ${entry.getTitle.toUpperCase}")
println("")

// start getting the description (which is the meaning of the word)
val descriptionAsHtml = entry.getDescription.getValue

// clean up the html with Jsoup
val jsoupDocument = Jsoup.parse(descriptionAsHtml)

// remove all anchor tags
jsoupDocument.select("a").remove()

// use this special formatter so the output is on multiple lines.
// the default formatter prints everything on one long line.
val jsoupFormatter = new JsoupFormatter
val documentAsPlainText = jsoupFormatter.getPlainText(jsoupDocument)
val finalCleanedDescription = replaceBadCharacters(documentAsPlainText.replaceAll("\n\n", "\n").trim)
println(finalCleanedDescription)

def replaceBadCharacters(string: String): String = {
    string.replaceAll("“", "\"")
          .replaceAll("”", "\"")
          .replaceAll("‘", "\"")
          .replaceAll("’", "\"")
          .replaceAll("&amp;", "&")
}


