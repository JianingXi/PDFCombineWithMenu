
def split_columns(df, max_total_width=200):
    """
    按照原始列顺序分组，确保每组宽度不超过 max_total_width。
    """
    est_widths = []
    for col in df.columns:
        col_strs = df[col].astype(str)
        avg_len = col_strs.map(len).mean()
        est_width = len(str(col)) + avg_len
        est_widths.append(est_width)

    groups = []
    current_group = []
    current_width = 0

    for col, width in zip(df.columns, est_widths):
        if current_group and current_width + width > max_total_width:
            groups.append(current_group)
            current_group = []
            current_width = 0
        current_group.append(col)
        current_width += width

    if current_group:
        groups.append(current_group)

    return groups