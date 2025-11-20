"""
Basic DAG validation tests for ML Pipeline

This test ensures the DAG can be loaded without errors and has the correct structure.
Run with: pytest tests/test_ml_pipeline_dag.py
"""

import unittest
from airflow.models import DagBag


class TestMLPipelineDAG(unittest.TestCase):
    """Basic validation tests for ML Pipeline DAG"""

    @classmethod
    def setUpClass(cls):
        """Load DAG bag once for all tests"""
        cls.dagbag = DagBag(dag_folder='dags/', include_examples=False)

    def test_dag_loaded(self):
        """Test if DAG is loaded without import errors"""
        dag = self.dagbag.get_dag(dag_id='mlpipeline_complete')
        
        # Check DAG exists
        self.assertIsNotNone(dag, "DAG 'mlpipeline_complete' not found")
        
        # Check no import errors
        self.assertEqual(
            len(self.dagbag.import_errors), 
            0,
            f"DAG import errors: {self.dagbag.import_errors}"
        )
        
        # Check expected number of tasks
        self.assertEqual(
            len(dag.tasks), 
            10, 
            f"Expected 10 tasks, found {len(dag.tasks)}"
        )

    def test_dag_has_tags(self):
        """Test DAG has appropriate tags"""
        dag = self.dagbag.get_dag(dag_id='mlpipeline_complete')
        self.assertIn('ml', dag.tags, "Missing 'ml' tag")
        self.assertIn('pipeline', dag.tags, "Missing 'pipeline' tag")


if __name__ == '__main__':
    unittest.main()
