#!/bin/sh
exec scala -savecompiled -classpath "lib/AtomReaderLibrary-assembly-1.0.jar" "$0" "$@"
!#

import java.net.{URL, URLConnection}
import com.rometools.rome.feed.synd.{SyndEntry, SyndFeed}
import com.rometools.rome.io.{SyndFeedInput, XmlReader}
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import com.alvinalexander.atom.JsoupFormatter
import scala.util.{Try,Success,Failure}
import scala.collection.JavaConverters._

// read the desired feed with ROME
val syndFeed: Try[SyndFeed] = Try {
    val urlConnection = getUrlConnection("https://www.merriam-webster.com/wotd/feed/rss2")
    val xmlReader = new XmlReader(urlConnection)
    val syndFeedInput = new SyndFeedInput
    syndFeedInput.build(xmlReader)
}

syndFeed match {
    case Success(feed) => {
        // convert it to a Scala `Seq`
        val entries: Seq[SyndEntry] = asScalaBuffer(feed.getEntries).toVector

        // the first entry is today's word of the day
        val entry: SyndEntry = entries(0)

        // print the word in a formatted way
        println(getWordFormatted(getWordOfDay(entry)))

        // start getting the description (which is the meaning of the word)
        val descriptionAsHtml = entry.getDescription.getValue

        // clean up the html with Jsoup
        val jsoupDocument: Document = Jsoup.parse(descriptionAsHtml)

        // remove all anchor tags from the document
        jsoupDocument.select("a").remove()

        // use this special formatter so the output is on multiple lines.
        // the default formatter prints everything on one long line.
        val jsoupFormatter = new JsoupFormatter
        val documentAsPlainText = jsoupFormatter.getPlainText(jsoupDocument)
        val finalCleanedDescription = documentAsPlainText.replaceAll("\n\n", "\n").trim
        println(finalCleanedDescription)
    }
    case Failure(e) => {
        println("\nCould not get the word of the day. Reason follows.")
        println(s"${e.getMessage}\n")
    }
}

def getUrlConnection(url: String): URLConnection = {
    val urlConnection = new URL(url).openConnection
    urlConnection.setConnectTimeout(5000)
    urlConnection.setReadTimeout(5000)
    urlConnection
}

def getWordOfDay(entry: SyndEntry): String = entry.getTitle.toUpperCase

def getWordFormatted(s: String): String = {
    s"""
      |
      |Word of the Day
      |---------------
      |Word: $s
    """.stripMargin
}



