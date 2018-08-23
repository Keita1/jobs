import aiohttp
import asyncio

'''
jobsites.py

This module provides wrapper classes for interacting with the some parts of the APIs of some job boards. 
Client code can simply provide a configuration file with the keys required to query each site, and receive job listings
as a response.

At the moment only two job boards are supported:
- The Muse
- Github Jobs

I intend to add more in the near future.
'''

# This browser header is provided if the API requires it.
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
}

# Exception classes.

class InvalidAPIKeyError(Exception):
    pass


class InvalidFieldError(Exception):
    pass


class APISpecificError(Exception):
    pass


async def _request(url, params):
    '''
    Asynchronously requests data from a particular board.
    Return value: Dictionary value parsed from a JSON string.
    '''
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, params=params) as resp:
            return await resp.json(encoding="UTF-8")


class GithubJobsWrapper:
    name = "Github"
    _url = "https://jobs.github.com"
    _endpoints = {
        "jobs": f"{_url}/positions.json",
        "job_id": f"{_url}/positions/"
    }
    _fields = ("description", "location", "lat", "long", "full_time", "page")

    @classmethod
    async def search(cls, endpoint, **kwargs):
        '''
        Queries an endpoint passed to the function, along with keyword arguments as the parameters.
        '''
        await cls._validate(endpoint, kwargs)
        return await _request(cls._endpoints[endpoint], params=kwargs)

    @classmethod
    async def findPosition(cls, id):
        '''
        Request a particular job posting.
        '''
        return await cls._request(cls._endpoints["job_id"] + id + ".json")

    @staticmethod
    async def listResults(resp):
        '''
        Additional generator, can be used to iterate through the results of a query.
        '''
        for result in resp:
            yield result

    @classmethod
    async def _validate(cls, endpoint, params):
        '''
        Ensure all required parameters are being passed, and no invalid parameters are supplied.
        '''

        keys = tuple(params.keys())

        if "lat" in keys or "long" in keys and not ("lat", "long") in keys:
            raise APISpecificError(
                "If latitude or longitude is provided, you must also provide the other as a parameter.")

        if ("lat", "long", "location") in keys:
            raise APISpecificError("If latitude and longitude parameters are provided, you must NOT additionally include\
            a location parameter.")

        # Check if required parameters are being passed, if not raise an error.
        for field in keys:
            if field not in cls._fields:
                raise InvalidFieldError(
                    f"The parameter {field} is not supported by Github Job's API.")


class TheMuseJobsWrapper:

    name = "TheMuse"
    _api_key = None
    _url = "https://themuse.com/api/public"
    _endpoints = {
        "jobs": {"URL": f"{_url}/jobs",
                 "fields": ("page", "descending", "company", "category", "level", "location")},
        "job_id": {"URL": f"{_url}/jobs/"},
        "companies": {"URL": f"{_url}/companies",
                      "fields": ("page", "descending", "industry", "size", "location")},
        "company_id": {"URL": f"{_url}/companies/"},
        "posts": {"URL": f"{_url}/posts",
                  "fields": ("page", "descending", "tag")},
        "post_id": {"URL": f"{_url}/posts/"},
        "coaches": {"URL": f"{_url}/coaches",
                    "fields": ("page", "descending", "offering", "level", "specialization")},
        "coach_id": {"URL": f"{_url}/coaches/"}
    }

    @classmethod
    def setKey(cls, key):
        cls._api_key = key

    # Append API key if it is there, otherwise validate then send!
    @classmethod
    async def search(cls, endpoint, **kwargs):
        await cls._validate(endpoint, kwargs)
        if cls._api_key is not None:
            kwargs["api_key"] = cls._api_key

        return await _request(cls._endpoints[endpoint]["URL"], params=kwargs)

    @classmethod
    async def findPosition(cls, endpoint, id):

        if cls._api_key:
            params = {"api_key": cls._api_key}

        return await _request(cls._endpoints[endpoint] + id, params=params)

    @staticmethod
    async def listResults(resp):
        '''
        Additional generator, can be used to iterate through the results of a query.
        '''
        for result in resp["results"]:
            yield result

    @classmethod
    async def _validate(cls, endpoint, params):
        '''
        Ensure all required parameters are being passed, and no invalid parameters are supplied.
        '''

        keys = tuple(params.keys())

        # Check if required parameters are being passed, if not raise an error.
        if "page" not in keys:
            raise APISpecificError(
                "The page number must be supplied as a parameter.")

        # Is the field a parameter that the endpoint permits? If not, then raise an error.
        for field in keys:
            if field not in cls._endpoints[endpoint]["fields"]:
                raise InvalidFieldError(
                    f"The parameter {field} for endpoint {endpoint} is not supported by The Muse's API.")
