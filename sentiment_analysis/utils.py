import requests

async def fetch_comments(skip: int, take: int, subscriber_id: int, access_token: str):
    """
    Retrieves dashboard metrics for user.
    This function fetches and returns the signing metrics for a given user.

    Args:
        owner_id (str): The ID of the owner.
        subscriber_id (int): The ID of the subscriber.
        access_token (str): The access token for authentication.

    Returns:
        dict: The entity metrics from the dashboard response.
    """
    url = f"https://document-poc.flowmono.com/api/Feedback/allfeedback/{skip}/{take}/{subscriber_id}"
    headers = {"Authorization": access_token}   
    
    try:
        response = requests.get(url, headers=headers)
        
        response.raise_for_status()
        
        metrics = response.json()
        
        return metrics["entity"]['entity']
    
    except requests.exceptions.RequestException as e:
        raise e
    
    except ValueError as e:
        raise e
    except Exception as e:
        raise e
