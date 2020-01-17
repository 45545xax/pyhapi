"""Summary

Attributes
----------
StorageTypeToSetAttrib : TYPE
    Description
"""
from ctypes import cdll, POINTER, c_int, c_int32, c_int64,\
    c_float, c_double, c_bool, byref, c_char_p, create_string_buffer
import asyncio
from datetime import datetime

import numpy as np

from . import hdata as HDATA

HAPI_LIB = cdll.LoadLibrary("libHAPIL")

def IsSessionValid(session):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    result = HAPI_LIB.HAPI_IsSessionValid(byref(session))
    return result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS

def Cleanup(session):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    """
    result = HAPI_LIB.HAPI_Cleanup(byref(session))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "Cleanup Failed with {0}".format(HDATA.HAPI_Result(result).name)


def CloseSession(session):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    """
    result = HAPI_LIB.HAPI_CloseSession(byref(session))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "Close Session Failed with {0}".format(HDATA.HAPI_Result(result).name)

def CreateInProcessSession(session):
    '''
    Attributes
    ----------
    session : HAPI_Session

    Returns
    -------
    bool: success

    Parameters
    ----------
    session : TYPE
        Description
    '''
    return HAPI_LIB.HAPI_CreateInProcessSession(byref(session))

def StartThriftNamedPipeServer(serverOptions):
    '''
    Attributes
    ----------
    serverOptions : HAPI_ThriftServerOptions

    Returns
    -------
    int: process id if success

    Parameters
    ----------
    serverOptions : TYPE
        Description
    '''
    processid = c_int32()
    result = HAPI_LIB.HAPI_StartThriftNamedPipeServer(\
        byref(serverOptions), c_char_p("hapi".encode('utf-8')), byref(processid))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "StartThriftNamedPipeServer Failed with {0}".format(HDATA.HAPI_Result(result).name)
    print("Session Created with Process Id: {0}".format(processid.value))
    return processid

def CreateThriftNamedPipeSession(session):
    '''
    Parameters
    ----------
    session : HAPI_Session
        Description
    '''
    result = HAPI_LIB.HAPI_CreateThriftNamedPipeSession(\
        byref(session), c_char_p("hapi".encode('utf-8')))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "CreateThriftNamedPipeSession Failed with {0}".format(HDATA.HAPI_Result(result).name)

def Initialize(session, cookOption, use_cooking_thread=True,\
    cooking_thread_stack_size=-1, houdini_environment_files="",\
        otl_search_path="", dso_search_path="",\
            image_dso_search_path="", audio_dso_search_path=""):
    '''
    Parameters
    ----------
    session : HAPI_Session
        Description
    cookOption : bool
        Description
    use_cooking_thread : bool, optional
        Description
    cooking_thread_stack_size : TYPE, optional
        Description
    houdini_environment_files : str, optional
        Description
    otl_search_path : str, optional
        Description
    dso_search_path : str, optional
        Description
    image_dso_search_path : str, optional
        Description
    audio_dso_search_path : str, optional
        Description
    '''
    result = HAPI_LIB.HAPI_Initialize(
        byref(session),
        byref(cookOption),
        c_bool(use_cooking_thread),
        c_int32(cooking_thread_stack_size),
        c_char_p(houdini_environment_files.encode('utf-8')),
        c_char_p(otl_search_path.encode('utf-8')),
        c_char_p(dso_search_path.encode('utf-8')),
        c_char_p(image_dso_search_path.encode('utf-8')),
        c_char_p(audio_dso_search_path.encode('utf-8')))
    assert result in (HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        HDATA.HAPI_Result.HAPI_RESULT_ALREADY_INITIALIZED),\
            "Initialize Failed with {0}".format(HDATA.HAPI_Result(result).name)


def LoadAssetLibraryFromFile(session, filePath, allow_overwrite=True):
    '''
    Attributes
    ----------
    session : HAPI_Session
    filePath : string
    library_id : int
    allow_overwrite : bool

    Returns
    -------
    int: asset library id if success

    Parameters
    ----------
    session : TYPE
        Description
    filePath : TYPE
        Description
    allow_overwrite : bool, optional
        Description
    '''
    assetLibId = c_int32()
    result = HAPI_LIB.HAPI_LoadAssetLibraryFromFile(\
        byref(session), c_char_p(filePath.encode('utf-8')),\
            c_bool(allow_overwrite), byref(assetLibId))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "LoadAssetLibraryFromFile Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return assetLibId

def _GetAvailableAssetCount(session, assetLibId):
    '''
    Attributes
    ----------
    session : HAPI_Session
    assetLibId : int

    Returns
    -------
    int: asset count if success

    Parameters
    ----------
    session : TYPE
        Description
    assetLibId : TYPE
        Description
    '''
    assetCount = c_int32()
    result = HAPI_LIB.HAPI_GetAvailableAssetCount(byref(session), assetLibId, byref(assetCount))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetAvailableAssetCount Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return assetCount

def GetAvailableAssets(session, assetLibId):
    '''
    Attributes
    ----------
    session : HAPI_Session
    assetLibId : int
    assetCount : int

    Returns
    -------
    string[]: asset names if success

    Parameters
    ----------
    session : TYPE
        Description
    assetLibId : TYPE
        Description
    '''
    assetCount = _GetAvailableAssetCount(session, assetLibId)

    asset_string_buffer = (c_int32 * assetCount.value)()

    result = HAPI_LIB.HAPI_GetAvailableAssets(\
        byref(session), assetLibId, byref(asset_string_buffer), assetCount)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetAvailableAssets Failed with {0}".format(HDATA.HAPI_Result(result).name)

    asset_names = []
    for i in range(0, len(asset_string_buffer)):
        asset_name = GetString(session, asset_string_buffer[i])
        asset_names.append(asset_name)

    return asset_names

def CreateInputNode(session, node_label):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_label : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    node_id = c_int32()
    result = HAPI_LIB.HAPI_CreateInputNode(\
        byref(session), byref(node_id), c_char_p(node_label.encode('utf-8')))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "CreateInputNode Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return node_id.value

def CreateNode(session, operator_name, node_label, parent_node_id=-1, cook_on_creation=False):
    '''
    Attributes
    ----------
    session : HAPI_Session
    operator_name: string
    node_label : string
    parent_node_id : int
    cook_on_creation : bool

    Returns
    -------
    int: node id if success

    Parameters
    ----------
    session : TYPE
        Description
    operator_name : TYPE
        Description
    node_label : TYPE
        Description
    parent_node_id : TYPE, optional
        Description
    cook_on_creation : bool, optional
        Description
    '''
    node_id = c_int32()
    result = HAPI_LIB.HAPI_CreateNode(\
        byref(session), c_int(parent_node_id), c_char_p(operator_name.encode('utf-8')),\
            c_char_p(node_label.encode('utf-8')), c_bool(cook_on_creation), byref(node_id))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "CreateNode Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return node_id.value

def DeleteNode(session, node_id):
    '''
    Attributes
    ----------
    session : HAPI_Session
    operator_name: string
    node_label : string
    parent_node_id : int
    cook_on_creation : bool

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description

    No Longer Returned
    ------------------
    int: node id if success
    '''
    result = HAPI_LIB.HAPI_DeleteNode(byref(session), node_id)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "DeleteNode Failed with {0}".format(HDATA.HAPI_Result(result).name)

def CookNode(session, cook_option, node_id):
    '''
    Attributes
    ----------
    session : HAPI_Session
    cook_option: HAPI_CookOptions
    node_id : int

    Parameters
    ----------
    session : TYPE
        Description
    cook_option : TYPE
        Description
    node_id : TYPE
        Description

    No Longer Returned
    ------------------
    int: node id if success
    '''
    result = HAPI_LIB.HAPI_CookNode(byref(session), node_id, byref(cook_option))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "CookNode Failed with {0}".format(HDATA.HAPI_Result(result).name)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(WaitCook(session))

async def CookNodeAsync(session, cook_option, node_id):
    '''
    Attributes
    ----------
    session : HAPI_Session
    cook_option: HAPI_CookOptions
    node_id : int

    Parameters
    ----------
    session : TYPE
        Description
    cook_option : TYPE
        Description
    node_id : TYPE
        Description

    No Longer Returned
    ------------------
    int: node id if success
    '''
    result = HAPI_LIB.HAPI_CookNode(byref(session), node_id, byref(cook_option))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "CookNodeAsync Failed with {0}".format(HDATA.HAPI_Result(result).name)
    await WaitCook(session)

async def WaitCook(session, statusReportInterval=1):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    statusReportInterval : int, optional
        Description
    """
    print("-------------Start Cooking!---------------")
    cookStatus = c_int32()
    cookResult = HDATA.HAPI_Result.HAPI_RESULT_ALREADY_INITIALIZED
    while True:
        cookResult = HAPI_LIB.HAPI_GetStatus(byref(session), 2, byref(cookStatus))
        continuestate = cookStatus.value > HDATA.HAPI_State.HAPI_STATE_MAX_READY_STATE\
            and cookResult == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS
        print("Cook Status at {0} : {1}".format(datetime.now().\
            strftime('%H:%M:%S'), _GetStatusString(session,\
            HDATA.HAPI_StatusType.HAPI_STATUS_COOK_STATE,\
                HDATA.HAPI_StatusVerbosity.HAPI_STATUSVERBOSITY_MESSAGES)))
        if not continuestate:
            break
        await asyncio.sleep(statusReportInterval)
    if cookStatus.value == HDATA.HAPI_State.HAPI_STATE_READY_WITH_FATAL_ERRORS:
        print("Cook with Fatal Error: {0}".format(_GetStatusString(session)))
    print("-------------Finish Cooking!---------------")
    assert cookResult == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS and\
        cookStatus.value == HDATA.HAPI_State.HAPI_STATE_READY,\
            "CookNode Failed with {0} and Cook Status is {1}".\
                format(HDATA.HAPI_Result(cookResult).name, HDATA.HAPI_State(cookStatus.value).name)

def QueryNodeInput(session, node_id, input_index=0):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        input_index (int, optional): [description]. Defaults to 0.

    Returns:
        [type]: [description]
    """
    connect_node_id = c_int32()
    result = HAPI_LIB.HAPI_QueryNodeInput(\
        byref(session), c_int(node_id), c_int(input_index), byref(connect_node_id))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "QueryNodeInput Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return connect_node_id.value

def ConnectNodeInput(session, node_id, node_id_to_connect, input_index=0, output_index=0):
    """[summary]
    
    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        node_id_to_connect ([type]): [description]
        input_index (int, optional): [description]. Defaults to 0.
        output_index (int, optional): [description]. Defaults to 0.
    """
    result = HAPI_LIB.HAPI_ConnectNodeInput(\
        byref(session), c_int(node_id), c_int(input_index),\
            c_int(node_id_to_connect), c_int(output_index))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "ConnectNodeInput Failed with {0}".format(HDATA.HAPI_Result(result).name)

def DisconnectNodeInput(session, node_id, input_index=0):
    """[summary]
    
    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        input_index (int, optional): [description]. Defaults to 0.
    """
    result = HAPI_LIB.HAPI_DisconnectNodeInput(byref(session), c_int(node_id), c_int(input_index))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "DisconnectNodeInput Failed with {0}".format(HDATA.HAPI_Result(result).name)

def GetComposedChildNodeList(session, node_id, count):
    id_buffer = ( c_int32 * count) ()
    result = HAPI_LIB.HAPI_GetComposedChildNodeList(\
        byref(session), node_id, byref(id_buffer), c_int(count))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetComposedChildNodeList Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return id_buffer

def ComposeChildNodeList(session, node_id,\
    node_type=HDATA.HAPI_NodeFlags.HAPI_NODEFLAGS_ANY,\
        node_flag=HDATA.HAPI_NodeFlags.HAPI_NODEFLAGS_ANY):
    '''
    Attributes
    ----------
    session : HAPI_Session
    node_id : int

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    '''
    childCount = c_int32()
    result = HAPI_LIB.HAPI_ComposeChildNodeList(\
        byref(session), node_id, c_int(node_type), c_int(node_flag),\
            c_bool(False), byref(childCount))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "ComposeChildNodeList Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return childCount.value

def GetDisplayGeoInfo(session, node_id):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]

    Returns:
        [type]: [description]
    """
    geo_info = HDATA.HAPI_GeoInfo()
    result = HAPI_LIB.HAPI_GetDisplayGeoInfo(byref(session), node_id, byref(geo_info))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetDisplayGeoInfo Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return geo_info

def GetPartInfo(session, node_id, part_id):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]

    Returns:
        [type]: [description]
    """
    part_info = HDATA.HAPI_PartInfo()
    result = HAPI_LIB.HAPI_GetPartInfo(byref(session), node_id, part_id, byref(part_info))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetPartInfo Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return part_info

def GetComposedObjectList(session, node_id, count):
    object_info_buffer = (HDATA.HAPI_ObjectInfo * count)()
    result = HAPI_LIB.HAPI_GetComposedObjectList(\
        byref(session), node_id, byref(object_info_buffer),\
            c_int(0),c_int(count))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetComposedObjectList Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return object_info_buffer

def ComposeObjectList(session, node_id):
    '''
    Attributes
    ----------
    session : HAPI_Session
    node_id : int

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    '''
    child_count = c_int32()
    result = HAPI_LIB.HAPI_ComposeObjectList(\
        byref(session), node_id, None, byref(child_count))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "ComposeObjectList Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return child_count.value

def GetNodeInfo(session, node_id):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    node_info = HDATA.HAPI_NodeInfo()
    result = HAPI_LIB.HAPI_GetNodeInfo(byref(session), node_id, byref(node_info))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetNodeInfo Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return node_info

def GetAssetInfo(session, node_id):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    asset_info = HDATA.HAPI_AssetInfo()
    result = HAPI_LIB.HAPI_GetAssetInfo(byref(session), c_int(node_id), byref(asset_info))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetAssetInfo Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return asset_info

def GetParameters(session, node_id, node_info):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    node_info : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    params = (HDATA.HAPI_ParmInfo * node_info.parmCount)()
    result = HAPI_LIB.HAPI_GetParameters(\
        byref(session), node_id, byref(params), c_int32(0), c_int32(node_info.parmCount))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetParameters Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return params

def GetParmIntValue(session, node_id, parmname, tupleid = 0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    parmname : TYPE
        Description
    tupleid : int, optional
        Description

    Returns
    -------
    TYPE
        Description
    """
    val = c_int32()
    result = HAPI_LIB.HAPI_GetParmIntValue(\
        byref(session), node_id, c_char_p(parmname.encode('utf-8')), tupleid, byref(val))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetParmIntValue Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return val.value

def GetParmFloatValue(session, node_id, parmname, tupleid = 0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    parmname : TYPE
        Description
    tupleid : int, optional
        Description

    Returns
    -------
    TYPE
        Description
    """
    val = c_float()
    result = HAPI_LIB.HAPI_GetParmFloatValue(\
        byref(session), node_id, c_char_p(parmname.encode('utf-8')), tupleid, byref(val))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetParmFloatValue Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return val.value

def GetParamStringValue(session, node_id, parmname, tupleid = 0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    parmname : TYPE
        Description
    tupleid : int, optional
        Description

    Returns
    -------
    TYPE
        Description
    """
    stringsh = c_int32()
    result = HAPI_LIB.HAPI_GetParmStringValue(\
        byref(session), node_id, c_char_p(parmname.encode('utf-8')), tupleid, True, byref(stringsh))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetParamStringValue Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return GetString(session, stringsh)

def SetParmIntValue(session, node_id, parmname, value, tupleid = 0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    parmname : TYPE
        Description
    value : TYPE
        Description
    tupleid : int, optional
        Description

    Returns
    -------
    TYPE
        Description
    """
    result = HAPI_LIB.HAPI_SetParmIntValue(\
        byref(session), node_id, c_char_p(parmname.encode('utf-8')), tupleid, value)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetParmIntValue Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetParmFloatValue(session, node_id, parmname, value, tupleid=0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    parmname : TYPE
        Description
    value : TYPE
        Description
    tupleid : int, optional
        Description

    Returns
    -------
    TYPE
        Description
    """
    result = HAPI_LIB.HAPI_SetParmFloatValue(\
        byref(session), node_id, c_char_p(parmname.encode('utf-8')), tupleid, value)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetParmFloatValue Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetParamStringValue(session, node_id, parmid, value, tupleid=0):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    parmid : TYPE
        Description
    value : TYPE
        Description
    tupleid : int, optional
        Description

    Returns
    -------
    TYPE
        Description
    """
    result = HAPI_LIB.HAPI_SetParmStringValue(\
        byref(session), node_id, c_char_p(value.encode('utf-8')), parmid, tupleid)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetParamStringValue Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetPartInfo(session, node_id, part_info):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    part_info : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    result = HAPI_LIB.HAPI_SetPartInfo(byref(session), node_id, 0, byref(part_info))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetPartInfo Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetCurveInfo(session, node_id, curve_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        curve_info ([type]): [description]
    """
    result = HAPI_LIB.HAPI_SetCurveInfo(byref(session), node_id, 0, byref(curve_info))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetCurveInfo Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetCurveCounts(session, node_id, part_id, curve_count):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        curve_count ([type]): [description]
    """
    intp = POINTER(c_int)
    result = HAPI_LIB.HAPI_SetCurveCounts(\
        byref(session), node_id, part_id,\
            curve_count.flatten().ctypes.data_as(intp), 0, curve_count.shape[0])
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetCurveCounts Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetCurveKnots(session, node_id, part_id, curve_knots):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        curve_knots ([type]): [description]
    """
    if type(curve_knots) == type(None):
        return
    intp = POINTER(c_int)
    result = HAPI_LIB.HAPI_SetCurveKnots(\
        byref(session), node_id, part_id,\
            curve_knots.flatten().ctypes.data_as(intp), 0, curve_knots.shape[0])
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetCurveKnots Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return

def AddAttribute(session, node_id, name, attrib_info):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    result = HAPI_LIB.HAPI_AddAttribute(\
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')), byref(attrib_info))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "AddAttribute Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetAttributeFloatData(session, node_id, name, attrib_info, data):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    data : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    floatp = POINTER(c_float)
    result = HAPI_LIB.HAPI_SetAttributeFloatData(\
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')),\
            byref(attrib_info), data.flatten().ctypes.data_as(floatp), 0, attrib_info.count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetAttributeFloatData Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetAttributeFloat64Data(session, node_id, name, attrib_info, data):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    data : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    floatp = POINTER(c_double)
    result = HAPI_LIB.HAPI_SetAttributeFloat64Data(\
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')),\
            byref(attrib_info), data.flatten().ctypes.data_as(floatp), 0, attrib_info.count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetAttributeFloatData Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetAttributeInt64Data(session, node_id, name, attrib_info, data):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    data : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    intp = POINTER(c_int64)
    result = HAPI_LIB.HAPI_SetAttributeInt64Data(\
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')),\
            byref(attrib_info), data.flatten().ctypes.data_as(intp), 0, attrib_info.count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetAttributeFloatData Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetAttributeIntData(session, node_id, name, attrib_info, data):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    data : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    intp = POINTER(c_int)
    result = HAPI_LIB.HAPI_SetAttributeIntData(\
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')),\
            byref(attrib_info), data.flatten().ctypes.data_as(intp), 0, attrib_info.count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetAttributeFloatData Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetAttributeStringData(session, node_id, name, attrib_info, data):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    name : TYPE
        Description
    attrib_info : TYPE
        Description
    data : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    charp = POINTER(c_char_p)
    result = HAPI_LIB. HAPI_SetAttributeStringData(\
        byref(session), node_id, 0, c_char_p(name.encode('utf-8')),\
            byref(attrib_info), data.flatten().ctypes.data_as(charp), 0, attrib_info.count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetAttributeFloatData Failed with {0}".format(HDATA.HAPI_Result(result).name)

StorageTypeToSetAttrib = {
    HDATA.HAPI_StorageType.HAPI_STORAGETYPE_INT     : SetAttributeIntData,
    HDATA.HAPI_StorageType.HAPI_STORAGETYPE_INT64   : SetAttributeInt64Data,
    HDATA.HAPI_StorageType.HAPI_STORAGETYPE_FLOAT   : SetAttributeFloatData,
    HDATA.HAPI_StorageType.HAPI_STORAGETYPE_FLOAT64 : SetAttributeFloat64Data,
    HDATA.HAPI_StorageType.HAPI_STORAGETYPE_STRING  : SetAttributeStringData
    }

def GetAttributeNames(session, node_id, part_info, attrib_type=HDATA.HAPI_AttributeOwner.HAPI_ATTROWNER_POINT):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_info ([type]): [description]
        attrib_type ([type], optional): [description].

    Returns:
        [type]: [description]
    """
    attrib_count = part_info.attributeCounts[attrib_type]
    string_handle_buffer = (c_int32 * attrib_count)()
    result = HAPI_LIB. HAPI_GetAttributeNames(\
        byref(session), node_id, part_info.id, attrib_type,\
            byref(string_handle_buffer), attrib_count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetAttributeNames Failed with {0}".format(HDATA.HAPI_Result(result).name)
    attrib_names = []
    for string_handle in string_handle_buffer:
        attrib_names.append(GetString(session, string_handle))
    return attrib_names


def GetAttributeInfo(session, node_id, part_id, name, attrib_type):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_type ([type]): [description]

    Returns:
        [type]: [description]
    """
    attrib_info = HDATA.HAPI_AttributeInfo()
    result = HAPI_LIB.HAPI_GetAttributeInfo(\
        byref(session), c_int(node_id), c_int(part_id),\
            c_char_p(name.encode('utf-8')), attrib_type, byref(attrib_info))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetAttributeInfo Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return attrib_info

def GetAttributeIntData(session, node_id, part_id, name, attrib_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_info ([type]): [description]

    Returns:
        [type]: [description]
    """
    data_buffer = ( c_int32 * (attrib_info.count * attrib_info.tupleSize))()
    result = HAPI_LIB.HAPI_GetAttributeFloatData(\
        byref(session), node_id, part_id, c_char_p(name.encode('utf-8')),\
            byref(attrib_info), -1,byref(data_buffer), 0, attrib_info.count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetAttributeIntData Failed with {0}".format(HDATA.HAPI_Result(result).name)
    data_np = np.frombuffer(data_buffer, np.int32)
    return np.reshape(data_np, (attrib_info.count, attrib_info.tupleSize))

def GetAttributeInt64Data(session, node_id, part_id, name, attrib_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_info ([type]): [description]

    Returns:
        [type]: [description]
    """
    data_buffer = (c_int64 * (attrib_info.count * attrib_info.tupleSize))()
    result = HAPI_LIB.HAPI_GetAttributeFloatData(\
        byref(session), node_id, part_id, c_char_p(name.encode('utf-8')),\
            byref(attrib_info), -1, byref(data_buffer), 0, attrib_info.count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetAttributeInt64Data Failed with {0}".format(HDATA.HAPI_Result(result).name)
    data_np = np.frombuffer(data_buffer, np.int64)
    return np.reshape(data_np, (attrib_info.count, attrib_info.tupleSize))

def GetAttributeFloatData(session, node_id, part_id, name, attrib_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_info ([type]): [description]

    Returns:
        [type]: [description]
    """
    data_buffer = ( c_float * (attrib_info.count * attrib_info.tupleSize))()
    result = HAPI_LIB.HAPI_GetAttributeFloatData(\
        byref(session), node_id, part_id, c_char_p(name.encode('utf-8')),\
            byref(attrib_info), -1, byref(data_buffer), 0, attrib_info.count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetAttributeFloatData Failed with {0}".format(HDATA.HAPI_Result(result).name)
    data_np = np.frombuffer(data_buffer, np.float32)
    return np.reshape(data_np, (attrib_info.count, attrib_info.tupleSize))

def GetAttributeFloat64Data(session, node_id, part_id, name, attrib_info):
    """
    """
    data_buffer = (c_double * (attrib_info.count * attrib_info.tupleSize))()
    result = HAPI_LIB.HAPI_GetAttributeFloatData(\
        byref(session), node_id, part_id, c_char_p(name.encode('utf-8')),\
            byref(attrib_info), -1,byref(data_buffer), 0, attrib_info.count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetAttributeFloat64Data Failed with {0}".format(HDATA.HAPI_Result(result).name)
    data_np = np.frombuffer(data_buffer, np.float64)
    return np.reshape(data_np, (attrib_info.count, attrib_info.tupleSize))

def GetAttributeStringData(session, node_id, part_id, name, attrib_info):
    """[summary]

    Args:
        session ([type]): [description]
        node_id ([type]): [description]
        part_id ([type]): [description]
        name ([type]): [description]
        attrib_info ([type]): [description]

    Returns:
        [type]: [description]
    """
    data_buffer = (c_char_p * (attrib_info.count * attrib_info.tupleSize))()
    result = HAPI_LIB.HAPI_GetAttributeFloatData(\
        byref(session), node_id, part_id, c_char_p(name.encode('utf-8')),\
            byref(attrib_info), -1, byref(data_buffer), 0, attrib_info.count)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetAttributeStringData Failed with {0}".format(HDATA.HAPI_Result(result).name)
    data_np = np.frombuffer(data_buffer, np.bytes_)
    return np.reshape(data_np, (attrib_info.count, attrib_info.tupleSize))

StorageTypeToGetAttrib = {
    HDATA.HAPI_StorageType.HAPI_STORAGETYPE_INT     : GetAttributeIntData,
    HDATA.HAPI_StorageType.HAPI_STORAGETYPE_INT64   : GetAttributeInt64Data,
    HDATA.HAPI_StorageType.HAPI_STORAGETYPE_FLOAT   : GetAttributeFloatData,
    HDATA.HAPI_StorageType.HAPI_STORAGETYPE_FLOAT64 : GetAttributeFloat64Data,
    HDATA.HAPI_StorageType.HAPI_STORAGETYPE_STRING  : GetAttributeStringData
    }

def SetVertexList(session, node_id, vertex_list_array):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    vertex_list_array : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    intp = POINTER(c_int)
    result = HAPI_LIB.HAPI_SetVertexList(\
        byref(session), node_id, 0, vertex_list_array.flatten().ctypes.data_as(intp),\
            0, np.size(vertex_list_array))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetVertexList Failed with {0}".format(HDATA.HAPI_Result(result).name)

def SetFaceCounts(session, node_id, face_counts_array):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    face_counts_array : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    intp = POINTER(c_int)
    result = HAPI_LIB.HAPI_SetFaceCounts(\
        byref(session), node_id, 0, face_counts_array.ctypes.data_as(intp),\
            0, face_counts_array.shape[0])
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SetFaceCounts Failed with {0}".format(HDATA.HAPI_Result(result).name)

def CommitGeo(session, node_id):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    node_id : TYPE
        Description
    """
    result = HAPI_LIB.HAPI_CommitGeo(byref(session), node_id)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "CommitGeo Failed with {0}".format(HDATA.HAPI_Result(result).name)


def SaveHIPFile(session, hipname, lock_nodes = False):
    '''
    Attributes
    ----------
    session : HAPI_Session
    hipname : string
    lock_nodes : bool

    Parameters
    ----------
    session : TYPE
        Description
    hipname : TYPE
        Description
    lock_nodes : bool, optional
        Description
    '''
    result = HAPI_LIB.HAPI_SaveHIPFile(\
        byref(session), c_char_p(hipname.encode('utf-8')), c_bool(lock_nodes))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "SaveHIPFile Failed with {0}".format(HDATA.HAPI_Result(result).name)

def GetCookOptions():
    """Summary

    Returns
    -------
    TYPE
        Description
    """
    cookOptions = HDATA.HAPI_CookOptions()
    cookOptions.splitGeosByGroup              = True
    cookOptions.splitGeosByAttribute          = False
    cookOptions.splitAttrSH                   = 0
    cookOptions.splitPointsByVertexAttributes = False
    cookOptions.cookTemplatedGeos             = True
    cookOptions.maxVerticesPerPrimitive       = 3
    cookOptions.refineCurveToLinear           = True
    cookOptions.curveRefineLOD                = 8
    cookOptions.packedPrimInstancingMode      = 2
    cookOptions.handleBoxPartTypes            = False
    cookOptions.handleSpherePartTypes         = False
    return cookOptions

def _GetStringBufLength(session, string_handle, buffer_length):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    string_handle : TYPE
        Description
    buffer_length : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    return HAPI_LIB.HAPI_GetStringBufLength(byref(session), string_handle, byref(buffer_length))

def _GetString(session, string_handle, string, length):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    string_handle : TYPE
        Description
    string : TYPE
        Description
    length : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    return HAPI_LIB.HAPI_GetString(byref(session), string_handle, string, length)

def GetString(session, string_handle):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    string_handle : TYPE
        Description

    Returns
    -------
    TYPE
        Description
    """
    bufferLength = c_int32()
    _GetStringBufLength(session, string_handle, bufferLength)
    buffers = create_string_buffer(bufferLength.value)
    _GetString ( session, string_handle, buffers, bufferLength )

    return buffers.value.decode()

def _GetStatusString(session, status=HDATA.HAPI_StatusType.HAPI_STATUS_COOK_RESULT,\
    verbosity=HDATA.HAPI_StatusVerbosity.HAPI_STATUSVERBOSITY_ERRORS):
    """Summary

    Parameters
    ----------
    session : TYPE
        Description
    status : TYPE, optional
        Description
    verbosity : TYPE, optional
        Description

    Returns
    -------
    TYPE
        Description
    """
    bufferLength = c_int32()
    result = HAPI_LIB.HAPI_GetStatusStringBufLength(byref(session), status, verbosity, byref(bufferLength))
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetStatusStringBufLength Failed with {0}".format(HDATA.HAPI_Result(result).name)
    buffers = create_string_buffer(bufferLength.value)
    result = HAPI_LIB.HAPI_GetStatusString(byref(session), status, buffers, bufferLength)
    assert result == HDATA.HAPI_Result.HAPI_RESULT_SUCCESS,\
        "GetStatusString Failed with {0}".format(HDATA.HAPI_Result(result).name)
    return buffers.value
