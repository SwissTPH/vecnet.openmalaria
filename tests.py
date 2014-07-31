import unittest,json
from experiment_creator_v2 import ExperimentDescription

__author__ = 'Alexander Vyushkov'


class TestExperimentDescription(unittest.TestCase):
    def setUp(self):
        pass

    @staticmethod
    def do_test(experiment):
        if isinstance(experiment, (str, unicode)):
            with open(experiment) as fp:
                exp = ExperimentDescription(fp)
        else:
            exp = experiment

        result = list(exp.scenarios())
        return result
        #self.assertEqual(len(result), len(expected_result), "Wrong number of scenario generated")  # Test for duplicates
        #self.assertEqual(set(result), expected_result, "experiment1.json test failed") # Test if content of scenarios is correct

    def test_initialization(self):
        self.assertRaises(TypeError, ExperimentDescription, 1)

    def test_dict(self):
        """ Testing experiment creation from a python dictionary.
        Simple case - all sweeps are already defined, no fully factorial product is required. """
        experiment = {"base": "<xml>@itn@ @irs@ </xml>",
                      "sweeps": {
                          "itn": {"itn 80": {"@itn@": "80"}, "itn 90": {"@itn@": "90"}},
                          "irs": {"irs 66": {"@irs@": "66"}, "irs 90": {"@irs@": "90"}}
                      },
                      "combinations": [
                          ["itn", "irs"],
                          ["itn 80", "irs 66"],
                          ["itn 80", "irs 90"],
                          ["itn 90", "irs 66"]
                      ]
                      }

        expected_result = ({u"<xml>80 66 </xml>",
                            u"<xml>80 90 </xml>",
                            u"<xml>90 66 </xml>", })
        exp = ExperimentDescription(experiment)
        self.assertEqual(exp.name, "Unnamed Experiment", "Wrong name")
        self.assertEqual("%s" % exp, "Unnamed Experiment", "Wrong name")

        result = self.do_test(exp)

        self.assertEqual(len(result), len(expected_result), "Wrong number of scenario generated")  # Test for duplicates
        self.assertEqual(set(result), expected_result, "experiment1.json test failed") # Test if content of scenarios is correct

    def test_str(self):
        """ Testing experiment creation from a python string """
        string = """{
            "name": "Experiment from a string",
            "base":"<xml> @itn@ </xml>",
            "sweeps": {
                "itn": {
                    "itn80": {
                        "@itn@":"80 @irs@"
                    },
                    "itn90": {
                        "@itn@": "@irs@ 90"
                    }
                },
                "irs": {
                    "irs66": {
                        "@irs@":"66"
                    },
                    "irs77": {
                        "@irs@": "77"
                    }
                }
             },
            "combinations":
            [
                ["itn", "irs"],
                ["itn80", "irs66"],
                ["itn80", "irs77"],
                ["itn90", "irs66"]
            ]
        }"""
        exp = ExperimentDescription(string)
        self.assertEqual(exp.name, "Experiment from a string", "Wrong name")
        expected_results = ({u"<xml> 80 66 </xml>",
                             u"<xml> 80 77 </xml>",
                             u"<xml> 66 90 </xml>", })
        result = self.do_test(exp)
        self.assertEqual(set(result), expected_results)

    def test_add_sweep_and_arms(self):
        """ Testing add_sweeps and add_arms functions
        """
        fp = open("experiment1.json", "r")
        exp=ExperimentDescription(json.load(fp))
        exp.experiment["base"] = "<xml> @itn@ @irs@ @model@ @p1@ (@p2@) </xml>"
        exp.add_sweep("test")
        exp.add_arm("test", "1", {"@p1@":2, "@p2@":"1"})
        exp.add_arm("test", "2", {"@p1@":1, "@p2@":"hey"})

        expected_result = ({u"<xml> 80 66 model1 2 (1) </xml>",
                            u"<xml> 80 66 model3 2 (1) </xml>",
                            u"<xml> 80 66 model2 2 (1) </xml>",
                            u"<xml> 80 66 model1 1 (hey) </xml>",
                            u"<xml> 80 66 model3 1 (hey) </xml>",
                            u"<xml> 80 66 model2 1 (hey) </xml>",
                            u"<xml> 80 77 model1 2 (1) </xml>",
                            u"<xml> 80 77 model3 2 (1) </xml>",
                            u"<xml> 80 77 model2 2 (1) </xml>",
                            u"<xml> 80 77 model1 1 (hey) </xml>",
                            u"<xml> 80 77 model3 1 (hey) </xml>",
                            u"<xml> 80 77 model2 1 (hey) </xml>",
                            u"<xml> 90 66 model1 2 (1) </xml>",
                            u"<xml> 90 66 model3 2 (1) </xml>",
                            u"<xml> 90 66 model2 2 (1) </xml>",
                            u"<xml> 90 66 model1 1 (hey) </xml>",
                            u"<xml> 90 66 model3 1 (hey) </xml>",
                            u"<xml> 90 66 model2 1 (hey) </xml>", })

        self.assertEqual(set(exp.scenarios()), expected_result)

    def test_1(self):
        with open("experiment1.json") as fp:
            exp = ExperimentDescription(fp)
        expected_result = ({u"<xml> 80 66 model1 </xml>",
                            u"<xml> 80 66 model3 </xml>",
                            u"<xml> 80 66 model2 </xml>",
                            u"<xml> 80 77 model1 </xml>",
                            u"<xml> 80 77 model3 </xml>",
                            u"<xml> 80 77 model2 </xml>",
                            u"<xml> 90 66 model1 </xml>",
                            u"<xml> 90 66 model3 </xml>",
                            u"<xml> 90 66 model2 </xml>"})
        result = list(exp.scenarios())
        self.assertEqual(exp.name, "Experiment 1")
        self.assertEqual(len(result), 9)  # Test for duplicates
        self.assertEqual(set(result), expected_result) # Test if content of scenarios is correct

    def test_2(self):
        results = self.do_test("experiment2.json")
        expected_results = ({u"<xml> 80 66 </xml>",
                             u"<xml> 80 77 </xml>",
                             u"<xml> 66 90 </xml>",})
        self.assertEqual(len(expected_results), len(results))
        self.assertEqual(set(results), expected_results)

    def test_3(self):
        results = self.do_test("experiment3.json")
        expected_results = ({
                                u"<xml> 80 66 1 1</xml>",
                                u"<xml> 80 77 2 2</xml>",
                                u"<xml> 66 90 1 1</xml>",
                            })
        self.assertEqual(len(expected_results), len(results))
        self.assertEqual(set(results), expected_results)

    def test_4(self):
        """ arm substitution string doesn't start and end with @ """
        self.assertRaises(TypeError, self.do_test, "experiment4.json")

    def test_5(self):
        expected_results = ({
            u"<xml> 66 90 1 2 dry</xml>",
            u"<xml> 77 90 1 2 dry</xml>",
            u"<xml> 80 66 1 2 dry</xml>",
            u"<xml> 80 77 1 2 dry</xml>",
            u"<xml> 66 90 2 2 wet</xml>",
            u"<xml> 77 90 2 2 wet</xml>",
            u"<xml> 80 66 2 2 wet</xml>",
            u"<xml> 80 77 2 2 wet</xml>",
            u"<xml> 66 90 2 2 </xml>",
            u"<xml> 77 90 2 2 </xml>",
            u"<xml> 80 66 2 2 </xml>",
            u"<xml> 80 77 2 2 </xml>",
            u"<xml> 66 90 3 2 dry</xml>",
            u"<xml> 77 90 3 2 dry</xml>",
            u"<xml> 80 66 3 2 dry</xml>",
            u"<xml> 80 77 3 2 dry</xml>",
            u"<xml> 80 66 1 2 wet</xml>",
            u"<xml> 80 66 1 2 dry</xml>",
            u"<xml> 80 66 1 2 </xml>",
            u"<xml> 80 66 3 2 wet</xml>",
            u"<xml> 80 66 3 2 dry</xml>",
            u"<xml> 80 66 3 2 </xml>",
            u"<xml> 80 66 2 2 wet</xml>",
            u"<xml> 80 66 2 2 dry</xml>",
            u"<xml> 80 66 2 2 </xml>",
            u"<xml> 80 77 1 2 wet</xml>",
            u"<xml> 80 77 1 2 dry</xml>",
            u"<xml> 80 77 1 2 </xml>",
            u"<xml> 80 77 3 2 wet</xml>",
            u"<xml> 80 77 3 2 dry</xml>",
            u"<xml> 80 77 3 2 </xml>",
            u"<xml> 80 77 2 2 wet</xml>",
            u"<xml> 80 77 2 2 dry</xml>",
            u"<xml> 80 77 2 2 </xml>",
            u"<xml> 66 90 1 2 wet</xml>",
            u"<xml> 66 90 1 2 dry</xml>",
            u"<xml> 66 90 1 2 </xml>",
            u"<xml> 66 90 3 2 wet</xml>",
            u"<xml> 66 90 3 2 dry</xml>",
            u"<xml> 66 90 3 2 </xml>",
            u"<xml> 66 90 2 2 wet</xml>",
            u"<xml> 66 90 2 2 dry</xml>",
            u"<xml> 66 90 2 2 </xml>",
        })

        results = self.do_test("experiment5.json")
        #self.assertEqual(len(expected_results), len(results))
        self.assertEqual(set(results), expected_results)

    def test_6(self):
        """Erin's experiment - first attempt to convert it to new JSON experiment description"""
        results = self.do_test("experiment6.json")
        self.assertEqual(len(results), 18)

    def test_7(self):
        """ Fully factorial experiment.
        Combinations defined as "[[],[]]"
        """
        results = self.do_test("experiment7.json")
        self.assertEqual(len(results), 27)

    def test_8(self):
        """ Fully factorial experiment.
        Combinations defined as "[]" shortcut
        """
        results = self.do_test("experiment8.json")
        self.assertEqual(len(results), 27)

    def test_9(self):
        """ All sweeps are defined in combinations"""
        expected_result = ({u"<xml> 80 66 model1 </xml>",
                            u"<xml> 80 77 model2 </xml>",
                            u"<xml> 90 66 model2 </xml>"})
        result = self.do_test("experiment9.json")
        self.assertEqual(len(result), 3)  # Test for duplicates
        self.assertEqual(set(result), expected_result) # Test if content of scenarios is correct

    def test_10(self):
        """ Fully factorial experiment.
        Combinations defined as "[]" shortcut
        """
        results = self.do_test("experiment10.json")
        self.assertEqual(len(results), 27)

if __name__ == "__main__":
    unittest.main()