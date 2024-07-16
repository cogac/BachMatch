const Papa = require("papaparse");
const { weaviate, dataType, generateUuid5 } =
 require("weaviate-client").default;

//async function populateWeaviate(){
// const client = await weaviate.connectToCustom(weavOptions);
// const supes = client.collections.get("scientific_supervisors");
// const supesExists = await supes.exists();
//	if (!supesExists) {
//		with supes.batch.dynamic() as batch:
//    for i, supervisor in enumerate(df.itertuples(index=False)):
//
//        data = {
//            "supe_id": supervisor.id_hash,
//            "fname": supervisor.fname,
//            "lname": supervisor.lname,
//            "statement": supervisor.statement,
//            "expertise": supervisor.expertise,
//            "cluster": supervisor.cluster
//
//        }
//
//        vector = json.loads(supervisor.vector)
//
//        batch.add_object(
//            properties=data,
//            uuid=generate_uuid5(supervisor.id_hash),
//            vector=vector  # Add the custom vector
//            # references=reference_obj  # You can add references here
//        )
//
//
//	}
//};
