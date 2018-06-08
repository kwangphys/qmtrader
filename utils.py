import pandas as pd

def parse_table(soup, exclude_incomplete_row=True):
    headers = [v.text for v in soup.find_all('th')]
    body = soup.find_all('tbody')
    if len(body) == 0:
        raise ValueError('Cannot find table body!')
    if len(body) > 1:
        raise ValueError('Multiple table boides!')
    body = body[0]
    rows = body.find_all('tr')
    row_values = []
    for row in rows:
        row_values.append([v.text for v in row.find_all('td')])
    if len(headers) == 0:
        headers = row_values[0]
        row_values = row_values[1:]
    header = headers[0]
    j = 0
    for i in range(1, len(headers)):
        if headers[i] == header:
            headers[i] = header + '_' + str(j)
            j += 1
        else:
            header = headers[i]
    if exclude_incomplete_row:
        ncol = len(headers)
        row_values = [v for v in row_values if len(v) == ncol]
    df = pd.DataFrame(columns=headers, data=row_values)
    df.set_index(headers[0], inplace=True, drop=True)
    return df


