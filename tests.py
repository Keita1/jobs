import asyncio
import aiohttp
import unittest
import jobs
from jobs import GithubJobsWrapper as testGJW
from jobs import TheMuseJobsWrapper as testTMJW


class SearchTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_GithubSearch(self):
        '''
        Verify that searching does work.
        '''

        async def test():
            searchResults = await testGJW.search("jobs",
                                                 description="Software Engineer",
                                                 location="New York City",
                                                 full_time="true"
                                                 )
            self.assertIsInstance(searchResults, list)
        self.loop.run_until_complete(test())

    def test_MuseSearch(self):
        '''
        Verify that searching does work.
        '''

        async def test():
            searchResults = await testTMJW.search("jobs",
                                                page="1",
                                                location="New York",
                                                )
            self.assertIsInstance(searchResults, dict)
        self.loop.run_until_complete(test())


class ResponseProcessingTest(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_GithubResponseProcessing(self):
        '''
        Tests processing class method (listResults) for the GithubJobs wrapper.
        '''

        async def test():
            searchResults = await testGJW.search("jobs",
                                                 description="Software Engineer",
                                                 location="New York City",
                                                 full_time="true"
                                                 )

            '''
            Remove comments if you want to see the results fly by.
            
            async for result in testGJW.listResults(searchResults):
                print(result)
            '''

        self.loop.run_until_complete(test())

    def test_MuseResponseProcessing(self):
        '''
        Tests processing class method (listResults) for the The Muse API wrapper.
        '''
        async def test():
            searchResults = await testTMJW.search("jobs",
                                                  page="1",
                                                  location="New York",
                                                  )
            '''
            Remove comments if you want to see the results fly by.

            async for result in testTMJW.listResults(searchResults):
                print(result)
            '''

        self.loop.run_until_complete(test())


class ValidationTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def test_GithubAPISpecificError1(self):
        '''
        Tests for an APISpecificError exception when both parameters lat and long are provided,
        but the location parameter has already been provided.
        '''
        async def test():
            await testGJW.search("jobs",
                                 description="Software Engineer",
                                 location="New York City",
                                 lat="40.7128",
                                 long="74.0060",
                                 full_time="true"
                                 )
        with self.assertRaises(jobs.APISpecificError):
            self.loop.run_until_complete(test())

    def test_GithubAPISpecificError2(self):
        '''
        Tests for an APISpecificError exception when either parameters lat or long are provided,
        but the other was not passed.
        '''
        async def test():
            await testGJW.search("jobs",
                                 description="Software Engineer",
                                 location="New York City",
                                 lat="40.7128",
                                 full_time="true"
                                 )
        with self.assertRaises(jobs.APISpecificError):
            self.loop.run_until_complete(test())

    def test_GithubInvalidFieldError(self):
        '''
        Tests for an InvalidFieldError exception when client code passes a field not supported 
        by the Github Jobs API.
        '''
        async def test():
            await testGJW.search("jobs",
                                 description="Software Engineer",
                                 location="New York City",
                                 invalidparameter="Despacito"
                                 )
        with self.assertRaises(jobs.InvalidFieldError):
            self.loop.run_until_complete(test())

    def test_MuseAPISpecificError1(self):
        '''
        Tests for APISpecificError when client code fails to provide a page keyword parameter to their query.
        '''
        async def test():
            await testTMJW.search("jobs",
                                 company="Google",
                                 location="New York City"
                                 )
        with self.assertRaises(jobs.APISpecificError):
            self.loop.run_until_complete(test())
    
    def test_MuseInvalidFieldError1(self):
        '''
        Tests for InvalidFieldError when client code provides a not-supported field to an endpoint in their query.
        '''
        async def test():
            await testTMJW.search("jobs",
                                    foo="bar",
                                    company="Google",
                                    location="New York City"
                                    )
        with self.assertRaises(jobs.APISpecificError):
            self.loop.run_until_complete(test())

if __name__ == '__main__':
    unittest.main()
