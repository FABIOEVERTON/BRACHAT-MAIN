#!/usr/bin/env python3
"""
OCI MCP Server - exposes OCI operations via MCP protocol
"""
import json
import sys
import os
from typing import Any, Dict, List

# Add OCI config path
oci_config_path = os.path.expanduser("~/.oci/config")

try:
    import oci
    from oci.config import from_file
    from oci.core import ComputeClient, VirtualNetworkClient, BlockstorageClient
    from oci.identity import IdentityClient
    from oci.object_storage import ObjectStorageClient
except ImportError:
    print(json.dumps({"error": "OCI SDK not installed"}), file=sys.stderr)
    sys.exit(1)

# Load OCI config
config = from_file(oci_config_path, "DEFAULT")

# Initialize clients
compute = ComputeClient(config)
vcn = VirtualNetworkClient(config)
block = BlockstorageClient(config)
identity = IdentityClient(config)
object_storage = ObjectStorageClient(config)

def handle_request(request: Dict) -> Dict:
    method = request.get("method")
    params = request.get("params", {})
    req_id = request.get("id")
    
    try:
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "oci-mcp", "version": "1.0"}
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {"name": "oci_list_instances", "description": "List compute instances", "inputSchema": {"type": "object", "properties": {"compartment_id": {"type": "string"}}, "required": ["compartment_id"]}},
                        {"name": "oci_list_vcns", "description": "List VCNs", "inputSchema": {"type": "object", "properties": {"compartment_id": {"type": "string"}}, "required": ["compartment_id"]}},
                        {"name": "oci_list_compartments", "description": "List compartments", "inputSchema": {"type": "object", "properties": {}}},
                        {"name": "oci_get_instance", "description": "Get instance details", "inputSchema": {"type": "object", "properties": {"instance_id": {"type": "string"}}, "required": ["instance_id"]}},
                        {"name": "oci_start_instance", "description": "Start instance", "inputSchema": {"type": "object", "properties": {"instance_id": {"type": "string"}}, "required": ["instance_id"]}},
                        {"name": "oci_stop_instance", "description": "Stop instance", "inputSchema": {"type": "object", "properties": {"instance_id": {"type": "string"}}, "required": ["instance_id"]}},
                        {"name": "oci_list_buckets", "description": "List object storage buckets", "inputSchema": {"type": "object", "properties": {"compartment_id": {"type": "string"}, "namespace": {"type": "string"}}, "required": ["compartment_id", "namespace"]}},
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = params.get("name")
            args = params.get("arguments", {})
            
            if tool_name == "oci_list_instances":
                compartment_id = args.get("compartment_id", config["tenancy"])
                instances = compute.list_instances(compartment_id).data
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps([{"id": i.id, "display_name": i.display_name, "lifecycle_state": i.lifecycle_state, "shape": i.shape, "region": config["region"]} for i in instances], indent=2)}]}}
            
            elif tool_name == "oci_list_vcns":
                compartment_id = args.get("compartment_id", config["tenancy"])
                vcns = vcn.list_vcns(compartment_id).data
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps([{"id": v.id, "display_name": v.display_name, "cidr_block": v.cidr_block, "state": v.lifecycle_state} for v in vcns], indent=2)}]}}
            
            elif tool_name == "oci_list_compartments":
                compartments = identity.list_compartments(config["tenancy"], compartment_id_in_subtree=True).data
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps([{"id": c.id, "name": c.name, "description": c.description, "state": c.lifecycle_state} for c in compartments], indent=2)}]}}
            
            elif tool_name == "oci_get_instance":
                instance_id = args["instance_id"]
                instance = compute.get_instance(instance_id).data
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps({"id": instance.id, "display_name": instance.display_name, "lifecycle_state": instance.lifecycle_state, "shape": instance.shape, "region": config["region"], "defined_tags": instance.defined_tags}, indent=2)}]}}
            
            elif tool_name == "oci_start_instance":
                instance_id = args["instance_id"]
                compute.instance_action(instance_id, "START")
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": f"Instance {instance_id} start requested"}]}}
            
            elif tool_name == "oci_stop_instance":
                instance_id = args["instance_id"]
                compute.instance_action(instance_id, "SOFTSTOP")
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": f"Instance {instance_id} stop requested"}]}}
            
            elif tool_name == "oci_list_buckets":
                compartment_id = args["compartment_id"]
                namespace = args["namespace"]
                buckets = object_storage.list_buckets(namespace, compartment_id).data
                return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps([{"name": b.name, "created_by": b.created_by, "time_created": str(b.time_created)} for b in buckets], indent=2)}]}}
            
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"}}
        
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown method: {method}"}}
    
    except Exception as e:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}), flush=True)

if __name__ == "__main__":
    main()
