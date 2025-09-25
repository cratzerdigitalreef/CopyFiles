# -*- coding: UTF-8 -*-

import os
import xml.etree.ElementTree as xmlManager
import xml.dom.minidom


# xml_utils_get_nodes ---------------------------------------------------------------------------------------------------------------------------------------------------------
def xml_utils_get_nodes(xml_path_with_file_name: str, node_name_to_find: str):
    """
        Retrieves all nodes with a specific name from an XML file and returns a list of dictionaries where each dictionary represents the elements it found from each node

    Args:
        xml_path_with_file_name (str): Path to the XML file to parse
        node_name_to_find (str): Name of the nodes to find in the XML structure

    Returns:
        tuple:

        if success: (True, nodes_found (List of dic), xml_absolute_path)

        if not success: (False, cause, '')

    Usage example:
        xml_utils_get_nodes(
            'directory/where/xml/file/will/be/created/xml_file_name.xml',
            'Command'
        )

    """
    # Check if file exists
    validation_result, cause, _, = __validate_file_path(xml_path_with_file_name)
    if not validation_result:
        return validation_result, cause, ''

    tree = xmlManager.parse(xml_path_with_file_name)
    root = tree.getroot()
    all_nodes = root.findall(node_name_to_find)
    nodes_list = []

    for node in all_nodes:
        data_in_node = node.attrib  # Get all attributes of the current node
        nodes_list.append(data_in_node)

    return True, nodes_list, xml_path_with_file_name


# xml_utils_get_header_nodes ---------------------------------------------------------------------------------------------------------------------------------------------------------
def xml_utils_get_elements_in_root_node(xml_path_with_file_name):
    """
    Retrieves the attributes of the root node in an XML file.

    Args:
        xml_path_with_file_name (str): Path to the XML file to parse

    Returns:
        tuple:

        if success: (True, root_attributes (dict), xml_absolute_path)

        if not success: (False, cause, '')

    Usage example:
        xml_utils_get_elements_in_root_node(
            'directory/where/xml/file/will/be/created/xml_file_name.xml'
        )

    """
    # Check if file exists
    validation_result, cause, _, = __validate_file_path(xml_path_with_file_name)
    if not validation_result:
        return validation_result, cause, ''

    tree = xmlManager.parse(xml_path_with_file_name)
    root = tree.getroot()
    attributes = root.attrib

    return True, attributes, xml_path_with_file_name


# xml_utils_write_nodes ---------------------------------------------------------------------------------------------------------------------------------------------------------
def xml_utils_write_nodes(xml_path_with_file_name: str, node_name: str, new_nodes_data: list[dict]):
    """
    Writes new nodes to an XML file directly under the existing xml root.

    Args:
        xml_path_with_file_name (str): Path to the XML file to modify
        node_name (str): Name of tne new node
        new_nodes_data (list of dict): List of dictionaries where each dictionary represents
                                      attributes for a new node to be added

    Returns:
        tuple:

        if success: (True, xml_content, xml_absolute_path)

        if not success: (False, cause, '')

    Usage example:
        xml_utils_write_nodes(
            'directory/where/xml/file/will/be/created/xml_file_name.xml',
            'Command',
            [{'NAME': 'Test1', 'CMD': 'B100'}, {'NAME': 'Test2', 'CMD': 'B101'}]
        )
    """
    validation_result, cause, _, = __validate_file_path(xml_path_with_file_name)
    if not validation_result:
        return validation_result, cause, ''

    try:
        # Parse the existing XML file
        tree = xmlManager.parse(xml_path_with_file_name)
        root = tree.getroot()

        # Create and add new nodes with their attributes
        for node_data in new_nodes_data:
            new_node = xmlManager.Element(node_name)  # Creates a generic node, you might want to customize this
            for key, value in node_data.items():
                new_node.set(key, str(value))
            root.append(new_node)

        # to format xml file
        xml_str = xmlManager.tostring(root, encoding="utf-8")
        xml_pretty = xml.dom.minidom.parseString(xml_str).toprettyxml()

        # It loops through the split XML lines and joins them together using '\n\n' as separator.
        # 'if line.strip()' Prevents the 'join' function from joining empty lines.
        xml_pretty = "\n\n".join([line for line in xml_pretty.split("\n") if line.strip()])

        # Write the modified tree back to the file

        with open(xml_path_with_file_name, "w", encoding="utf-8") as f:
            f.write(xml_pretty)
        return True, xml_pretty, xml_path_with_file_name

    except Exception as e:
        cause = f"Error writing to XML file: {str(e)}"
        return False, cause, ''


# xml_utils_create_file ---------------------------------------------------------------------------------------------------------------------------------------------------------
def xml_utils_create_file(header_name: str,
                          header_attrs: dict,
                          child_node_name: str,
                          child_nodes_data: list[dict],
                          dir_path: str = '',
                          name: str = ''
                          ):
    """
    Creates a new XML file with specified root and child nodes structure.

    Args:
        header_name (str): Name of the root XML element
        header_attrs (dict): Dictionary of attributes for the root element
        child_node_name (str): Name to use for child nodes
        child_nodes_data (list[dict]): List of dictionaries containing child nodes' attributes
        dir_path (str): The directory where the file will be located
        name (str): The name of the xml file

    Returns:
        tuple:

        if success: (True, xml_content, xml_absolute_path)

        if not success: (False, cause, '')

    Usage example:
        xml_utils_create_file(
            'xml_to_test_applet',
            {'VERSION' : '1.0'},
            'Command',
            [{'NAME': 'Test1', 'CMD': 'B100'}, {'NAME': 'Test2', 'CMD': 'B101'}],
            'directory/where/xml/file/will/be/created/',
            'xml_file_name'
        )
    """
    if not dir_path:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = os.path.dirname(dir_path)

    if name:
        name = name.replace(' ', '_')
        if name[-4:].lower() != '.xml':
            name += '.xml'
    else:
        name = 'default_name.xml'

    if not os.path.isdir(dir_path):
        cause = f'xml_utils_create_file.py: dir_path argument is not a directory => {dir_path}'
        return False, cause, ''

    xml_path = os.path.join(dir_path, name)

    try:
        # Create root element with attributes
        root = xmlManager.Element(header_name)
        for attr, value in header_attrs.items():
            root.set(attr, str(value))

        # Add child nodes with their attributes
        for node_data in child_nodes_data:
            child_node = xmlManager.SubElement(root, child_node_name)
            for attr, value in node_data.items():
                child_node.set(attr, str(value))
        # to format xml file
        xml_str = xmlManager.tostring(root, encoding="utf-8")
        xml_pretty = xml.dom.minidom.parseString(xml_str).toprettyxml()

        # It loops through the split XML lines and joins them together using '\n\n' as separator.
        # 'if line.strip()' Prevents the 'join' function from joining empty lines.
        xml_pretty = "\n\n".join([line for line in xml_pretty.split("\n") if line.strip()])
        # Write to file (using binary mode to handle encoding properly)

        with open(xml_path, 'w') as f:
            f.write(xml_pretty)
        return True, xml_pretty, xml_path

    except Exception as e:
        cause = f"xml_utils_create_file.py: Failed to create XML file: {str(e)}"
        return False, cause, ''

def __validate_file_path(xml_path_with_file_name):

    # Check if file exists
    if not os.path.exists(xml_path_with_file_name):
        cause = f"xml_utils_write_nodes.py: File not found: {xml_path_with_file_name}"
        return False, cause, ''

    if not os.path.isfile(xml_path_with_file_name):
        cause = f'The xml_path_with_file_name argument is not a file: {xml_path_with_file_name}'
        return False, cause, ''

    if xml_path_with_file_name[-4:].lower() != '.xml':
        cause = f'The xml_path_with_file_name argument is not a .XML file: {xml_path_with_file_name}'
        return False, cause, ''

    return True, '', ''

# TO TEST ---------------------------------------------------------------------------------------------------------------------------------------------------------
def xml_utils_general_test(xml_path_test_create: str, xml_path_with_file_name: str):
    """
    Executes examples of methods xml_utils_get_nodes, xml_utils_create_file, xml_utils_write_nodes, xml_utils_get_elements_in_root_node

    Args:
        xml_path_test_create (str): path where to create files,
        xml_path_with_file_name (str): path with file name to test getters
    Returns:
        void
    """

    root_attr_example = {
        'NAME': "Protocol tests for the SapAuth applet, OTA channel",
        'VERSION': "1.0"
    }

    new_node_name = 'Command'

    new_node_dic = {
        'PACKAGE': "sapauth.methods.key_management.OTA.ota_clear_all_keys",
        'CLIENT': "T-MOBILE",
        'TPDA': "05810601F4",
        'COMMAND': "B105",
        'COMMAND_DESCRIPTION': "this command was added from the code",
        'LOG_FILE_NAME': "clear_keys_p2_not_present",
        'ERROR_EXPECTED': "false"
    }
    new_nodes_list = [new_node_dic]

    print(xml_utils_get_nodes(xml_path_with_file_name, 'Command'))
    print(xml_utils_get_elements_in_root_node(xml_path_with_file_name))
    print(xml_utils_write_nodes(xml_path_with_file_name, 'Command', new_nodes_list))
    print(xml_utils_create_file('OtaFullTest', root_attr_example, new_node_name, new_nodes_list, xml_path_test_create,
                                'test_name_argument_espaced_2 '))

# xml_path_test_w_f_n = r"C:\Users\darie\Siprocal\Proyectos\Python\QA_APPLET_FRAMEWORK\applet-sapauth-qafrmw\sapauth\automated_tests\OTA\execution_configurations\default_name.xml"
# xml_path_test_ = r"C:\Users\darie\Siprocal\Proyectos\Python\QA_APPLET_FRAMEWORK\applet-sapauth-qafrmw\sapauth\automated_tests\OTA\execution_configurations"
# xml_path_test_create_ = r"C:\Users\darie\Siprocal\Proyectos\Python\QA_APPLET_FRAMEWORK\applet-sapauth-qafrmw\sapauth\automated_tests\OTA\execution_configurations\tests_protocol_ota_sapauth-full.xml"
#
# xml_utils_general_test(xml_path_test_, xml_path_test_create_,xml_path_test_w_f_n)
def xml_utils_replace_node(xml_path_with_file_name: str, node_name: str, value: str):
    """
    Replaces the value of a node if it exists, or adds it if not. Ensures no duplicates of the node.
    """
    if not os.path.exists(xml_path_with_file_name):
        return False, f"File not found: {xml_path_with_file_name}", ""

    try:
        tree = xmlManager.parse(xml_path_with_file_name)
        root = tree.getroot()

        # Remove all existing nodes with the same name
        for elem in list(root):
            if elem.tag == node_name:
                root.remove(elem)

        # Create and append the updated node
        new_node = xmlManager.Element(node_name)
        new_node.set("value", value)
        root.append(new_node)

        # Format and save
        xml_str = xmlManager.tostring(root, encoding="utf-8")
        xml_pretty = xml.dom.minidom.parseString(xml_str).toprettyxml()
        xml_pretty = "\n\n".join([line for line in xml_pretty.split("\n") if line.strip()])

        with open(xml_path_with_file_name, "w", encoding="utf-8") as f:
            f.write(xml_pretty)

        return True, xml_pretty, xml_path_with_file_name

    except Exception as e:
        return False, f"Error updating XML: {str(e)}", ""
