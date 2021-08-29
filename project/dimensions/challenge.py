from .models import Company, Dimension
from collections import defaultdict

# Tree Node for in-memory reperestaion of the dimensions and its children
# For each company will be a list of  parent dimensions (root nodes)
class TreeNode:
    def __init__(self, dimensionId):
        self.id = dimensionId
        self.children = []


# idDimensionMap - Key = Dimension id ; Value = Dimension Object
idDimensionMap = defaultdict(Dimension)

# idTreeNodeMap  - Key = dimension id of the top level Dimensions(has no parent); Value = TreeNode of child dimensions
idTreeNodeMap = defaultdict(TreeNode)

# Recursive function to get all child nodes for a given node
def dfs_db(name, step):
    result = []
    tab = ""
    for i in range(step):
        tab += "\t"
    result.append(tab + name)
    # Dimension.objects.filter(parent__name=name).values('name') : Query to get the list of child dimensions
    # for a given parent
    for dimensionName in Dimension.objects.filter(parent__name=name).values('name'):
        result.extend(dfs_db(dimensionName["name"],  step + 1))
    return result

def list_children(dimension_id):
    """ List a dimension and all its children in a nested hierarchy. """
    # Query to get dimension name for the given dimension id from db
    dimension_name = list(Dimension.objects.filter(id=dimension_id).values('name'))
    # DFS function to call recursively all child dimension for the given dimension id
    return dfs_db(dimension_name[0]["name"], 0)


def dfs(node, step):
    result = []
    tab = ""
    for _ in range(step):
        tab += "\t"
    result.append(tab + idDimensionMap[node.id]["name"])
    for child in node.children:
        result.extend(dfs(child,  step + 1))
    return result

# Function to create idTreeNodeMap, list of top level dimensions in a tree data structure.
def createInMemoryMaps(company_id):
    rootDimensions = []
    # Dimension.objects.filter(company__id=company_id).values() -
    #     Sql to get list of dimensions for a given company id
    for dimension in Dimension.objects.filter(company__id=company_id).values():
        idDimensionMap[dimension["id"]] = dimension
        if dimension["parent_id"] is None:
            rootDimensions.append(dimension)
            if dimension["id"] not in idTreeNodeMap:
                node = TreeNode(dimension["id"])
                idTreeNodeMap[dimension["id"]] = node
        else:
            if dimension["parent_id"] not in idTreeNodeMap:
                node = TreeNode(dimension["parent_id"])
                idTreeNodeMap[dimension["parent_id"]] = node
            if dimension["id"] not in idTreeNodeMap:
                childNode = TreeNode(dimension["id"])
                idTreeNodeMap[dimension["id"]] = childNode
            idTreeNodeMap[dimension["parent_id"]].children.append(idTreeNodeMap[dimension["id"]])
    return rootDimensions

def list_hierarchy(company_id):
    """ List the complete nested hierarchy for a company. """
    result = []
    # Get all root dimensions for a given company
    rootDimensions = createInMemoryMaps(company_id)
    for child in rootDimensions:
        node = idTreeNodeMap[child["id"]]
        result.extend(dfs(node, 0))
    return result


