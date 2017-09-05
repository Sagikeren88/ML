@pytest.mark.labels('s3_emd_func')
def test_emd_single_attr_update_expression_existing_item(self, setup):
    """
    Perform an update expression on an existing single item:
    Preparation:
    Put new item
    update:
    update single item (should succeed)
    check:
    Verify update is as expected (should succeed)
    """
    # Preparation
    bucket = self.container
    table = "table"
    key = {"ID": {"N": "100"}}
    items = {"Age": {"N": "42"}, "Country": {"S": "UK"}, "Name": {"S": "Eric"}
        , "Deceased": {"BOOL": False}, "Signature": {"B": "RXJpY0NsYXB0b24="}}
    packed_items = pack_put_item(key=key, attributes=items)
    packed_get_items = pack_get_item(table=table, key=key, attrs_to_get="*")
    update_expression = "Age=Age+1"
    packed_expression = pack_put_item(update_mode='CreateOrReplaceAttributes', update_expression=update_expression)

    TestS3EMDFunc.conn.put_item(bucket=bucket, table=table, item=packed_items)

    # Update expression
    TestS3EMDFunc.conn.put_item(bucket=bucket, table=table, key_value=key['ID']['N'], item=packed_expression)

    # check
    res = TestS3EMDFunc.conn.get_item(bucket=bucket, item=packed_get_items)
    assert int(res['Item']['Age']['N']) == int(items['Age']['N']) + 1


@pytest.mark.labels('s3_emd_func')
def test_emd_multiple_attr_update_expressions_existing_item(self, setup):
    """
    Perform multiple update expressions on an existing item:
    Preparation:
    Put new item
    update:
    update multiple items from several types (should succeed)
    check:
    Verify updates are as expected (should succeed)
    """
    # Preparation
    bucket = self.container
    table = "table"
    key = {"ID": {"N": "100"}}
    items = {"Age": {"N": "42"}, "Country": {"S": "UK"}, "Name": {"S": "Eric"}
        , "Deceased": {"BOOL": False}, "Signature": {"B": "RXJpY0NsYXB0b24="}}
    packed_items = pack_put_item(key=key, attributes=items)
    packed_get_items = pack_get_item(table=table, key=key, attrs_to_get="*")
    update_expression = "Age=Age+1, Country=IL, Name=Clapton, Deceased=True, Signature=Q2xhcHRvbkVyaWM="
    packed_expression = pack_put_item(update_mode='CreateOrReplaceAttributes', update_expression=update_expression)

    TestS3EMDFunc.conn.put_item(bucket=bucket, table=table, item=packed_items)

    # Update expression
    TestS3EMDFunc.conn.put_item(bucket=bucket, table=table, key_value=key['ID']['N'], item=packed_expression)

    # check
    res = TestS3EMDFunc.conn.get_item(bucket=bucket, item=packed_get_items)
    assert int(res['Item']['Age']['N']) == int(items['Age']['N']) + 1
    assert res['Item']['Country']['S'] == 'IL'
    assert res['Item']['Name']['S'] == 'Clapton'
    assert res['Item']['Deceased']['BOOL'] is True
    assert res['Item']['Signature']['B'] == 'Q2xhcHRvbkVyaWM='





def pack_put_item(table=None, key=None, condition=None, attributes=None, update_mode=None, update_expression=None):
    # type: (str, dict[str,str], str, dict[str,dict[str,str]]) -> dict
    item = {}
    if table is not None:
        item['TableName'] = table
    if key is not None:
        item['Key'] = key
    if condition is not None:
        item['ConditionExpression'] = condition
    if update_mode is not None:
        item['UpdateMode'] = update_mode
    if update_expression:
        item['UpdateExpression'] = update_expression
    if attributes:
        item['Item'] = {}
        for attr, definition in attributes.iteritems():
            item['Item'][attr] = {}
            for key, value in definition.iteritems():
                item['Item'][attr][key] = value
    return item