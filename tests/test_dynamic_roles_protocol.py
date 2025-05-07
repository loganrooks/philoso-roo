import unittest
from unittest.mock import patch, mock_open, call
import json

# Assume a simplified representation of how clinerules might be parsed and executed
# For testing, we'll simulate the relevant parts of the orchestrator and analysis modes.

class MockAnalysisMode:
    def propose_dynamic_role_update(self, material_id, context_id, role):
        # This method would, in a real scenario, use the `new_task` tool.
        # We'll simulate the payload it would send.
        proposal_payload = {
            "request_type": "manage_dynamic_roles_update",
            "material_id": material_id,
            "role_object": {
                "context_id": context_id,
                "role": role
            }
        }
        # Simulate calling new_task by directly calling a (mocked) orchestrator handler
        return MockPhilosophyOrchestrator().handle_dynamic_roles_update_proposal(proposal_payload)

class MockPhilosophyOrchestrator:
    def handle_dynamic_roles_update_proposal(self, proposal):
        # This is the method that needs to be implemented based on the protocol.
        # For TDD, it will initially be missing or incomplete.
        # It should:
        # 1. Receive the proposal.
        # 2. Read master_index.json.
        # 3. Update dynamic_roles for the material_id in master_index.json.
        # 4. Write master_index.json.
        # 5. Determine the path to the material-specific index.md.
        # 6. Read the material-specific index.md.
        # 7. Update dynamic_roles in the material-specific index.md.
        # 8. Write the material-specific index.md.
        
        # Minimal implementation to make the first test fail meaningfully
        if proposal.get("request_type") == "manage_dynamic_roles_update":
            # Simulate failure or incomplete implementation
            # raise NotImplementedError("Dynamic roles update handling not implemented in orchestrator")
            # For now, let's assume it tries to do something but fails at file ops
            
            material_id = proposal["material_id"]
            role_object = proposal["role_object"]

            # --- master_index.json processing ---
            master_index_path = "source_materials/processed/master_index.json"
            material_index_path_template = "source_materials/processed/library/{}/index.md" # Simplified for test
            
            # This part will be mocked in tests
            with open(master_index_path, 'r+') as f:
                data = json.load(f)
                updated = False
                for item in data.get("materials", []):
                    if item.get("id") == material_id:
                        if "dynamic_roles" not in item:
                            item["dynamic_roles"] = []
                        # Avoid duplicate role_objects for the same context_id if already present
                        # This is a simplified check; a more robust check might compare dicts
                        if not any(r.get("context_id") == role_object.get("context_id") for r in item["dynamic_roles"]):
                            item["dynamic_roles"].append(role_object)
                        updated = True
                        break
                if not updated: # If material_id not found, add it
                    if "materials" not in data:
                        data["materials"] = []
                    data["materials"].append({"id": material_id, "title": f"Title for {material_id}", "dynamic_roles": [role_object]}) # Added title for consistency
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()

            # --- material-specific index.md processing ---
            material_specific_path = material_index_path_template.format(material_id)
            try:
                with open(material_specific_path, 'r+') as f: # This will fail if file doesn't exist
                    # Simplified: assume YAML frontmatter and append to it
                    # Real implementation would need proper YAML parsing and writing
                    content = f.read() # Read existing content
                    # Placeholder for actual YAML update logic.
                    # For TDD, we'll make it write something simple to check the write call.
                    # A more robust test would mock YAML parsing and check the structure.
                    new_role_string_for_test = f"\n- context_id: {role_object['context_id']}\n  role: {role_object['role']}\n"
                    
                    # This is a naive append for testing purposes, not proper YAML update.
                    # The test will verify that a write attempt is made.
                    # The actual content verification will drive better implementation.
                    updated_content = content # In a real scenario, parse YAML, update, then serialize
                    
                    # Let's assume for now we are just appending to a known section or creating it
                    # This is still very simplified.
                    if "dynamic_roles:" in updated_content:
                        # Crude append for testing
                        updated_content += new_role_string_for_test
                    else:
                        # Crude creation for testing
                        updated_content += "\ndynamic_roles:\n" + new_role_string_for_test.lstrip()

                    f.seek(0)
                    f.write(updated_content)
                    f.truncate()
            except FileNotFoundError:
                # If the file doesn't exist, create it with the new role
                # This is also a simplified handling for TDD progression
                with open(material_specific_path, 'w') as f:
                    # Crude creation for testing
                    f.write("---\n")
                    f.write(f"id: {material_id}\n")
                    f.write("title: New Material (Created by Test)\n") # Placeholder title
                    f.write("dynamic_roles:\n")
                    f.write(f"  - context_id: {role_object['context_id']}\n    role: {role_object['role']}\n")
                    f.write("---\n")
                    f.write("Initial content.\n")


            # Simulate a successful operation for now, tests will verify mocks
            return {"status": "success", "message": "Dynamic role update processed (simulated)."}
        
        return {"status": "failure", "message": "Unknown request type."}


class TestDynamicRolesProtocol(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('json.load')
    def test_orchestrator_receives_and_attempts_master_index_update(self, mock_json_load, mock_json_dump, mock_file_open):
        """
        Test Case 2 (Failing): philosophy-orchestrator correctly receives and
        attempts to process manage_dynamic_roles_update proposals by reading/writing master_index.json.
        This test will initially fail because the orchestrator's handler is not fully implemented.
        """
        orchestrator = MockPhilosophyOrchestrator()
        proposal = {
            "request_type": "manage_dynamic_roles_update",
            "material_id": "test_material_001",
            "role_object": {"context_id": "inquiry_abc", "role": "primary_source"}
        }

        # Simulate existing master_index.json content
        mock_json_load.return_value = {"materials": [{"id": "test_material_001", "title": "Test Material 1", "dynamic_roles": []}]}
        
        result = orchestrator.handle_dynamic_roles_update_proposal(proposal)
        
        self.assertEqual(result["status"], "success") # Assuming success for now if no error
        
        # Verify master_index.json was opened for read and then write
        mock_file_open.assert_any_call("source_materials/processed/master_index.json", 'r+')
        
        # Verify json.load was called (to read existing data)
        mock_json_load.assert_called_once()
        
        # Verify json.dump was called (to write updated data)
        expected_master_data = {"materials": [{"id": "test_material_001", "title": "Test Material 1", "dynamic_roles": [{"context_id": "inquiry_abc", "role": "primary_source"}]}]}
        # The actual call to json.dump will be with a file object, so we check the data passed.
        # The first argument to dump is the data, the second is the file pointer.
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        self.assertEqual(args[0], expected_master_data)

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load') # For master_index.json
    @patch('json.dump') # For master_index.json
    # We need a separate mock for reading/writing the YAML/Markdown index.md
    # For simplicity, we'll mock 'open' again but control its return value based on path
    def test_orchestrator_attempts_material_specific_index_update(self, mock_json_dump_master, mock_json_load_master, mock_file_open_specific):
        """
        Test Case 4 (Failing): philosophy-orchestrator attempts to perform
        synchronized writes to the material-specific index.md.
        """
        orchestrator = MockPhilosophyOrchestrator()
        proposal = {
            "request_type": "manage_dynamic_roles_update",
            "material_id": "test_material_002",
            "role_object": {"context_id": "essay_xyz", "role": "secondary_source"}
        }

        # Simulate master_index.json read/write as it's part of the flow
        mock_json_load_master.return_value = {"materials": [{"id": "test_material_002", "title": "Test Material 2"}]}
        
        # Simulate existing material-specific index.md content (simplified)
        # This mock needs to handle different files being opened.
        # We'll use side_effect to return different mock objects for different paths.
        
        mock_master_index_file = mock_open(read_data=json.dumps({"materials": [{"id": "test_material_002", "title": "Test Material 2"}]})).return_value
        mock_material_index_file = mock_open(read_data="---\ntitle: Test Material 2\nid: test_material_002\ndynamic_roles:\n---\nContent").return_value

        def file_open_side_effect(path, mode='r'):
            if path == "source_materials/processed/master_index.json":
                return mock_master_index_file
            elif path == "source_materials/processed/library/test_material_002/index.md":
                return mock_material_index_file
            raise FileNotFoundError(f"Unexpected file open: {path}")

        mock_file_open_specific.side_effect = file_open_side_effect
        
        result = orchestrator.handle_dynamic_roles_update_proposal(proposal)
        self.assertEqual(result["status"], "success")

        # Verify material-specific index.md was opened for read and then write
        # This assertion will likely fail until the orchestrator logic is implemented
        # to actually open and write to this file.
        
        # Check calls to open
        # Expected calls: master_index.json (r+), material_specific_index.md (r+)
        # The exact number and order might vary based on implementation details.
        # For now, let's assert it was called for the material specific file.
        
        # Check that the material specific file was opened for read/write or write (if new)
        # The mock_file_open_specific is the factory for file mocks.
        # We need to check its call_args_list.
        
        material_specific_path = "source_materials/processed/library/test_material_002/index.md"
        
        # Check if it was opened with 'r+' or 'w'
        opened_for_read_write = any(
            call_args[0][0] == material_specific_path and call_args[0][1] == 'r+'
            for call_args in mock_file_open_specific.call_args_list
        )
        opened_for_write_new = any(
            call_args[0][0] == material_specific_path and call_args[0][1] == 'w'
            for call_args in mock_file_open_specific.call_args_list
        )
        self.assertTrue(opened_for_read_write or opened_for_write_new,
                        f"Material-specific index.md ({material_specific_path}) was not opened for 'r+' or 'w'. Calls: {mock_file_open_specific.call_args_list}")

        # More detailed check: verify what was written to the material-specific file.
        # This requires inspecting the calls to the write() method of the mock file object.
        
        # Find the mock file object for the material-specific path
        written_content = ""
        handle = None
        # Need to access the correct mock object returned by the side_effect
        # This part of the test needs careful handling of how mock_open_specific.side_effect works
        # and how to retrieve the specific mock file handle for 'material_specific_path'.

        # Iterate through calls to the mock_open_specific factory
        for call_obj in mock_file_open_specific.call_args_list:
            path_arg, mode_arg = call_obj[0] # call_obj[0] is the tuple of positional args
            if path_arg == material_specific_path:
                # Get the mock file handle that was returned for this path
                # This assumes mock_open_specific(path, mode) returns the handle directly
                # or that the side_effect function returns it.
                # Our current side_effect returns mock_material_index_file or mock_master_index_file
                if path_arg == "source_materials/processed/library/test_material_002/index.md":
                    handle = mock_material_index_file # from the test setup
                break
        
        if handle:
            # Consolidate all writes to this handle
            for call_arg in handle.write.call_args_list: # This accesses the .write mock on the file handle
                written_content += call_arg[0][0]
        
            # Assert that the new role is present in the written content (simplified check)
            self.assertIn("context_id: essay_xyz", written_content)
            self.assertIn("role: secondary_source", written_content)
            self.assertIn("dynamic_roles:", written_content) # Ensure the section is there
        else:
            self.fail(f"Could not get a mock handle for {material_specific_path} to check written content. Check mock_file_open_specific setup.")

    @patch('tests.test_dynamic_roles_protocol.MockPhilosophyOrchestrator.handle_dynamic_roles_update_proposal')
    def test_analysis_mode_proposes_update_to_orchestrator(self, mock_orchestrator_handler):
        """
        Test Case 1 (Failing initially if MockAnalysisMode is not set up to call orchestrator):
        Analysis mode correctly proposes dynamic_roles update to philosophy-orchestrator.
        """
        analysis_mode = MockAnalysisMode()
        
        # Expected payload for the orchestrator
        expected_proposal = {
            "request_type": "manage_dynamic_roles_update",
            "material_id": "hegel_phen_intro_processed",
            "role_object": {"context_id": "current_inquiry_XYZ", "role": "primary_source"}
        }
        mock_orchestrator_handler.return_value = {"status": "success_from_orchestrator_mock"}

        result = analysis_mode.propose_dynamic_role_update(
            material_id="hegel_phen_intro_processed",
            context_id="current_inquiry_XYZ",
            role="primary_source"
        )
        
        mock_orchestrator_handler.assert_called_once_with(expected_proposal)
        self.assertEqual(result, {"status": "success_from_orchestrator_mock"})


if __name__ == '__main__':
    unittest.main()