import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import lab_traffic_generator

class TestValidation(unittest.TestCase):
    def test_validate_lab_ip_valid(self):
        self.assertTrue(lab_traffic_generator.validate_lab_ip("192.168.56.129"))
        self.assertTrue(lab_traffic_generator.validate_lab_ip("192.168.56.1"))
        self.assertTrue(lab_traffic_generator.validate_lab_ip("192.168.56.254"))

    def test_validate_lab_ip_invalid(self):
        self.assertFalse(lab_traffic_generator.validate_lab_ip("192.168.1.1"))
        self.assertFalse(lab_traffic_generator.validate_lab_ip("8.8.8.8"))
        self.assertFalse(lab_traffic_generator.validate_lab_ip("10.0.0.5"))
        self.assertFalse(lab_traffic_generator.validate_lab_ip("192.168.57.129"))
        
    def test_validate_lab_ip_malformed(self):
        self.assertFalse(lab_traffic_generator.validate_lab_ip("not-an-ip"))
        self.assertFalse(lab_traffic_generator.validate_lab_ip("192.168.56.999"))

if __name__ == '__main__':
    unittest.main()
