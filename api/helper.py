import json
from datetime import datetime


def prepare_response(query_result, context):
    result = {}
    metadatum = []
    for res in query_result:
        story_metadata = res[0] if len(res) > 0 else None

        if story_metadata is not None:

            if 'app_id' not in result.keys():
                result['app_id'] = story_metadata.app_id

            if 'timestamp' not in result.keys():
                timestamp = int(round(datetime.now().timestamp()))
                result['timestamp'] = timestamp

            metadatum_obj = {}
            metadatum_obj['id'] = story_metadata.story_id

            try:
                story_meta_dict = json.loads(story_metadata.metadata_)
            except json.decoder.JSONDecodeError:
                context.logger.error(f"Error with story {story_metadata.story_id} metadata format")

            metadatum_obj['metadata'] = story_meta_dict['img'] if story_metadata is not None and 'img' in story_meta_dict.keys() else None
            metadatum.append(metadatum_obj)

    result['metadata'] = metadatum

    return result
