# jobs
**Wrapper classes for asynchronously interacting with the APIs of job boards.**

## Supported Job Boards

At the moment only Github Jobs and The Muse's Developer API are supported. This list will be added on to in the near future.

* [https://jobs.github.com/api](Github Jobs API) - No API key required
* [https://www.themuse.com/developers/api/v2](The Muse API - V2) - API key optional

Boards requiring use of a key have or will have a special method setKey() for their respective classes.

And as a **important** note, **please be respectful and act within limits when querying sites.**

## Requirements

The following modules are required to use the classes within this module:

* `asyncio`
* `aiohttp`

These are contained in `requirements.txt`. In addition, if you want to test this module, the `unittest` module is required (but that's already included in the Python standard library).

You can install all of these dependencies by running the following command:

`pip install -r requirements.txt`




