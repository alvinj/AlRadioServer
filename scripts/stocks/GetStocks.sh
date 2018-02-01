#!/bin/sh
exec scala -savecompiled -classpath "./StockQuotes2018-assembly-1.0.jar" "$0" "$@"
!#

import net.liftweb.json.DefaultFormats
import net.liftweb.json._
import scala.collection.mutable.ArrayBuffer
import com.alvinalexander.stockquotes._

// use LinkedHashMap because i want it sorted by key
val stockMap = scala.collection.mutable.LinkedHashMap(
    "CAT"  -> Stock("CAT",  169, 0),
    "CELG" -> Stock("CELG", 102, 0),
    "FB"   -> Stock("FB",   179, 0),
    "GE"   -> Stock("GE",    19, 0),
    "IRBT" -> Stock("IRBT",  70, 0),
    "JD"   -> Stock("JD",    46, 0),
    "KMI"  -> Stock("KMI",   18, 0),
    "PAYC" -> Stock("PAYC",  92, 0),
    "PFE"  -> Stock("PFE",   36, 0),
    "SPY"  -> Stock("SPY",  283, 0)
)

// creates "CAT,CELG,FB,GE,IRBT,JD,KMI,PAYC,PFE"
val mapKeysForUri = stockMap.keySet.toVector.sorted.mkString(",")

//NOTE AlphaVantage does not return anything for VLKAY
val jsonString = NetworkUtils.get(
    s"https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols=${mapKeysForUri}&apikey=API_KEY_HERE",
    10*1000,
    10*1000
)

val json = parse(jsonString)

implicit val formats = DefaultFormats

val elements = (json \\ "Stock Quotes").children

val stocks = ArrayBuffer[Stock]()
// keys are: "1. symbol", "2. price", "3. volume", "4. timestamp"
for (i <- 0 until stockMap.size) {
    val e = elements(0)(i)
    // Map(1. symbol -> MSFT, 2. price -> 91.6000, 3. volume -> 23511825, 4. timestamp -> 2018-01-22...)
    val values = e.values.asInstanceOf[Map[String,String]]   //coercion
    val symbol = values("1. symbol")
    val oldStock = stockMap(symbol)
    oldStock.currentPrice = values("2. price").trim.toDouble
    stockMap(symbol) = oldStock
}

//TODO this formatting should be done in another script. i should just return the data.
for ((symbol,stock) <- stockMap) {
    val boughtAtString = f"(${stock.priceIBoughtAt}%.2f)"
    val boughtAt = f"$boughtAtString%10s"
    println(f"${stock.symbol}%-6s  ${stock.currentPrice}%10.2f $boughtAt                         .")
    println("")
}
println("                                                      .")

case class Stock(
    symbol: String,
    priceIBoughtAt: Double,
    var currentPrice: Double
)


