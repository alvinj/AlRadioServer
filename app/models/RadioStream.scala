package models

case class RadioStream (streamname: String, filename: String)

object RadioStream {

    import play.api.libs.json._

    implicit object RadioStreamFormat extends Format[RadioStream] {

        // from JSON string to a RadioStream object (de-serializing from JSON)
        def reads(json: JsValue): JsResult[RadioStream] = {
            val name = (json \ "name").as[String]
            // TODO i don't care about the `null` here, this method is only needed to make the api happy
            JsSuccess(RadioStream(name, null))
        }

        // convert from RadioStream object to JSON (serializing to JSON).
        // clients don't need to worry about the filename, so i don't emit it here.
        def writes(stream: RadioStream): JsValue = {
            val listOfStreams = Seq(
                "name" -> JsString(stream.streamname) 
            )
            JsObject(listOfStreams)
        }

    } 

}


