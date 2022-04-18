from django.test import TestCase


class AlgorithmsTest(TestCase):
    def test_fibonacci_valid_input(self):
        """fibonacci valid input"""
        response = self.client.post(path='http://host.docker.internal/algorithm/fibonacci/', data={'number': 10})
        self.assertEqual(response.status_code, 200)
        result = int(response.json()['result'])
        self.assertEqual(34, result)

    def test_fibonacci_invalid_input(self):
        """fibonacci invalid input"""
        response = self.client.post(path='http://host.docker.internal/algorithm/fibonacci/', data={'number': "10zx"})
        self.assertEqual(response.status_code, 400)
        response = response.json()
        self.assertEqual(response['status'], False)

    def test_fibonacci_negative_input(self):
        """fibonacci negative input"""
        response = self.client.post(path='http://host.docker.internal/algorithm/fibonacci/', data={'number': -10})
        self.assertEqual(response.status_code, 400)
        response = response.json()
        self.assertEqual(response['status'], False)

    def test_fibonacci_large_number(self):
        response = self.client.post(path='http://host.docker.internal/algorithm/fibonacci/', data={'number': 1000})
        self.assertEqual(response.status_code, 200)
        response = response.json()
        actual_answer = "26863810024485359386146727202142923967616609318986952340123175997617981700247881689338369654483356564191827856161443356312976673642210350324634850410377680367334151172899169723197082763985615764450078474174626"
        self.assertEqual(response['result'], int(actual_answer))

    def test_factorial_valid_input(self):
        """factorial valid input"""
        response = self.client.post(path='http://host.docker.internal/algorithm/factorial/', data={'number': 5})
        self.assertEqual(response.status_code, 200)
        result = int(response.json()['result'])
        self.assertEqual(120, result)

    def test_factorial_invalid_input(self):
        """factorial invalid input"""
        response = self.client.post(path='http://host.docker.internal/algorithm/factorial/', data={'number': "10zx"})
        self.assertEqual(response.status_code, 400)
        response = response.json()
        self.assertEqual(response['status'], False)

    def test_factorial_negative_input(self):
        """factorial negative input"""
        response = self.client.post(path='http://host.docker.internal/algorithm/factorial/', data={'number': -10})
        self.assertEqual(response.status_code, 400)
        response = response.json()
        self.assertEqual(response['status'], False)

    def test_factorial_large_number(self):
        """test large factorial number"""
        response = self.client.post(path='http://host.docker.internal/algorithm/factorial/', data={'number': 1000})
        self.assertEqual(response.status_code, 200)
        response = response.json()
        import math
        actual_answer = math.factorial(1000)
        self.assertEqual(response['result'], int(actual_answer))

    def test_ackermann_valid_input(self):
        """ackermann valid input"""
        response = self.client.post(path='http://host.docker.internal/algorithm/ackermann/', data={'m': 4, 'n': 1})
        self.assertEqual(response.status_code, 200)
        result = int(response.json()['result'])
        self.assertEqual(49, result)

    def test_ackermann_invalid_input(self):
        """ackermann invalid input"""
        response = self.client.post(path='http://host.docker.internal/algorithm/ackermann/', data={'m': "10zx", 'n' : 1})
        self.assertEqual(response.status_code, 400)
        response = response.json()
        self.assertEqual(response['status'], False)

    def test_ackermann_negative_input(self):
        """ackermann negative input"""
        response = self.client.post(path='http://host.docker.internal/algorithm/ackermann/', data={'m': -10, 'n':1})
        self.assertEqual(response.status_code, 400)
        response = response.json()
        self.assertEqual(response['status'], False)

    def test_ackermann_large_number(self):
        """test large ackermann number"""
        response = self.client.post(path='http://host.docker.internal/algorithm/ackermann/', data={'m': 5,'n': 7})
        self.assertEqual(response.status_code, 200)
        response = response.json()
        actual_answer = 6141004759
        self.assertEqual(response['result'], actual_answer)
