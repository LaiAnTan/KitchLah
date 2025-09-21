import boto3, json, base64
from datetime import datetime
from bson import ObjectId

kinesis = boto3.client("kinesis", region_name="ap-southeast-1")
stream_name = "kitchlah-orders-stream"

order = {
	"orderID": "1",
	"datetime": str(datetime.now()),
	"items": [
		{
			"item_id": "68cfbac49cd6acf342686777",
			"quantity": 1,
			"remarks": "More Spaghetti"
		},
		{
			"item_id": "68cfbac49cd6acf342686778",
			"quantity": 4,
			"remarks": "More Chicken Chop"
		}
	]
}

def kinesis_put(client, order):

	response = kinesis.put_record(
		StreamName=stream_name,
		Data=json.dumps(order),
		PartitionKey="retaurant1"
	)

	print(response)

def kinesis_view(client):

	shards = client.describe_stream(StreamName=stream_name)["StreamDescription"]["Shards"]
	for shard in shards: # theres more than one shard ya fuck
		shardId = shard["ShardId"]
		print(shardId)

		iterator = client.get_shard_iterator(
			StreamName=stream_name,
			ShardId=shardId,
			ShardIteratorType="TRIM_HORIZON",
		)["ShardIterator"]

		records = client.get_records(ShardIterator=iterator, Limit=5)
		for r in records["Records"]:
			data = json.loads(r["Data"].decode("utf-8"))
			print(data)

if __name__ == "__main__":
	kinesis_put(kinesis, order)
	# kinesis_view(kinesis)