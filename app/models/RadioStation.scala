package models

case class RadioStation (number: BigDecimal, description: String)

object RadioStation {

    import play.api.libs.json._

    implicit object RadioStationFormat extends Format[RadioStation] {

        // from JSON string to a RadioStation object (de-serializing from JSON)
        def reads(json: JsValue): JsResult[RadioStation] = {
            val number = (json \ "number").as[BigDecimal]
            val description = (json \ "description").as[String]
            JsSuccess(RadioStation(number, description))
        }

        // convert from RadioStation object to JSON (serializing to JSON)
        def writes(station: RadioStation): JsValue = {
            val listOfStations = Seq(
                "number" -> JsNumber(station.number), 
                "description" -> JsString(station.description)
            )
            JsObject(listOfStations)
        }

    } 

}


