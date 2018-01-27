#!/bin/sh
exec scala -savecompiled -classpath "lib/AtomReaderLibrary-assembly-1.0.jar" "$0" "$@"
!#

// script takes two params: 1) feed name, 2) feed url

import java.net.URL
import com.rometools.rome.feed.synd.SyndFeed
import com.rometools.rome.io.SyndFeedInput
import com.rometools.rome.io.XmlReader
import org.jsoup.Jsoup
import scala.collection.JavaConverters._
import util.control.Breaks._

val feedName = args(0)
val feedUrlString = args(1)

val feedUrl = new URL(feedUrlString)
val input = new SyndFeedInput
val feed: SyndFeed = input.build(new XmlReader(feedUrl))

// `feed.getEntries` has type `java.util.List[SyndEntry]`
val entries = asScalaBuffer(feed.getEntries)

var count = 0
var page = 1
breakable {
    for (entry <- entries) {
        if (count == 0 || count % 5 == 0) {
            println(s"\n(($feedName - $page))")
            println("----------------\n")
            page += 1
        }
        println(entry.getTitle)
        println("")
        count += 1
        // print a maximum of 20 headlines
        if (count > 20) break
    }
}


