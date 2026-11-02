import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    print(event)
    tenant_id = event['body']['tenant_id']
    texto = event['body']['texto']
    nombre_tabla = os.environ["TABLE_NAME"]
    nombre_bucket = os.environ["BUCKET_NAME"]

    # Proceso
    uuidv1 = str(uuid.uuid1())
    comentario = {
        'tenant_id': tenant_id,
        'uuid': uuidv1,
        'detalle': {
            'texto': texto
        }
    }

    # Guardar en DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(nombre_tabla)
    response = table.put_item(Item=comentario)

    # Ingesta Push: grabar el JSON como archivo en S3
    s3 = boto3.client('s3')
    key = f"{tenant_id}/{uuidv1}.json"
    s3.put_object(
        Bucket=nombre_bucket,
        Key=key,
        Body=json.dumps(comentario, ensure_ascii=False),
        ContentType='application/json'
    )

    # Salida (json)
    print(comentario)
    return {
        'statusCode': 200,
        'comentario': comentario,
        'response': response,
        's3_bucket': nombre_bucket,
        's3_key': key
    }