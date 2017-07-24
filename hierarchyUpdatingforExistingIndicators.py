def main():
    # importing required modules
    import pandas as pd
    import datetime

    date_today = datetime.date.today().isoformat()

    # getting user input for data files

    main_file = input("""What's the filename of the main hierarchy.indicators CSV file to be updated?
                      Note that this code assumes that this CSV uses the standard format for hierarchy.indicator file.""")
    add_file = input("""What's the filename of the CSV file which contains the indicator name, id, and categories to
                     be added to the main hierarchy file?
                     
                     Note that this code assumes that this CSV has the following columns:
                     ['Indicator Name', 'Display Name', 'Dataset', 'catlev_1', 'catlev_2',
       'catlev_3', 'catlev_4', 'catlev_5']""")


    # Load Data
    df_add = pd.read_csv(add_file + '.csv')
    df_main = pd.read_csv(main_file + '.csv',
                          usecols=['Indicator ID', 'Indicator Name', 'Display Name', 'Dataset',
                                   'Value Type Slug', 'Value Type Descriptor', 'Units', 'Rank 1',
                                   'Category 1 - slug', 'Category 1.1', 'Category 1.2', 'Category 1.3',
                                   'Category 1.4', 'Category 1.5', 'Rank 2', 'Category 2 - slug',
                                   'Category 2.1', 'Category 2.2', 'Category 2.3', 'Category 2.4',
                                   'Category 2.5', 'Rank 3', 'Category 3 - slug', 'Category 3.1',
                                   'Category 3.2', 'Category 3.3', 'Category 3.4', 'Category 3.5',
                                   'Rank 4', 'Category 4 - slug', 'Category 4.1', 'Category 4.2',
                                   'Category 4.3', 'Category 4.4', 'Category 4.5'])

    # generate the current number of hierarchies attached to each indicator.
    lev1_cols = ['Category %d.1' % (lev) for lev in range(1, 5)]
    df_main['current_hierarchy_num'] = df_main[lev1_cols].notnull().sum(axis=1)

    error_ctr = 0
    for row in df_add.index:
        try:
            id_val = str(df_add.loc[row, 'Indicator Name'])
            index = df_main[df_main['Indicator ID'] == str(df_add.loc[row, 'Indicator Name'])].index[0]

        except:
            try:
                disp_val = df_add.loc[row, 'Display Name']
                index = df_main[df_main['Display Name'] == str(df_add.loc[row, 'Display Name'])].index[0]
                print("No ID match for Indicator Name %s in main file." % str(id_val))
            except:
                print("No ID match for %s or Display Name match %s in main file." % (str(id_val),disp_val))
                error_ctr += 1
                continue

        curr_hier = df_main.loc[index, 'current_hierarchy_num']

        for lev in range(1, 6):
            df_main.loc[index, "Category %s.%d" % (str(curr_hier + 1), lev)] = df_add.loc[row, 'catlev_%s' % lev]

        # update the current_hierarchy for each hierarchy added
        # (since it's possible to have 2 additional hierarchies for the same indicator)
        df_main.loc[index, 'current_hierarchy_num'] = curr_hier + 1

    print("%d additional hierarchy(ies) have (has) been successfully added into the main indicator file." % (len(df_add.index) - error_ctr))
    print("%d error(s) were (was) encountered." % error_ctr)

    df_main.drop(['current_hierarchy_num'], axis=1, inplace=True)

    final_file = "%s-hierarchy.indicators-final.csv" % date_today
    df_main.to_csv(final_file, index=False, line_terminator='\r')
    print("Updated hierarchy file saved as %s" % final_file)

if __name__ == '__main__':
    main()