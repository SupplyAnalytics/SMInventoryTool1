import pandas as pd
import mysql.connector
from github import Github
import base64


def connection():
    print('Connection Established')
    mydb = mysql.connector.connect(
        user='skreadonlyuser_api',
        host='report-reader.cluster-custom-c8oe0gvszktr.ap-south-1.rds.amazonaws.com',
        password='XUerT9JxnWnEstSA'
    )

    cursor = mydb.cursor()
    print('Data Fetching')
    cursor.execute(''' select 
    vss.variantid variantid, 
    vss.sizeid sizeid,
    szm.sizetext sizetext,
    p.productname productname, 
    sm.companyname sellername,
    upper(cm.name) as SubCategory, 
    upper(cm2.name) as SuperCategory, 
    vss.quantity Stock_quantity, 
    case when sm.sellertype = 'BRAND_AGGREGATORS' then 'PP' else 'DP' end as Platform, 
    od1.GMV as GMV, 
    od1.GMV_PerDay GMV_PerDay, 
    dense_rank() over (partition by concat(vss.variantid,'_', vss.sizeid) order by od1.GMV_PerDay desc) as pareto_rank
    from 
    shoekonnect_live.variant_size_stock vss
    left join shoekonnect_live.variants v on vss.variantid = v.variantid
    left join shoekonnect_live.products p on v.productid = p.productid
    LEFT JOIN shoekonnect_live.category_master AS  cm ON cm.categoryid  = p.subcategoryid
    LEFT JOIN shoekonnect_live.category_master AS  cm1 ON cm1.categoryid  = cm.parentid
    LEFT JOIN shoekonnect_live.category_master AS  cm2 ON cm2.categoryid  = cm1.parentid
    left join shoekonnect_live.seller_master sm on p.sellerid = sm.userid 
    left join shoekonnect_live.size_master szm on vss.sizeid = szm.sizeid
    left join 
    (
    select 
    distinct 
    concat(od.variantid,'_',od.sizeid) as concat, 
    sum((od.skPrice -od.couponDiscount + od.sellerdiscount + od.shipping + od.shippingTaxAmt -
    od.shippingDiscount+od.shippingMarginDiscountApplied -od.advDiscount) * od.setSize * od.SetCount) as gmv, 
    sum((od.skPrice -od.couponDiscount + od.sellerdiscount + od.shipping + od.shippingTaxAmt -
    od.shippingDiscount+od.shippingMarginDiscountApplied -od.advDiscount) * od.setSize * od.SetCount) / 30 as GMV_PerDay
    from 
    shoekonnect_live.orders o
    left join shoekonnect_live.order_details od on o.orderid = od.orderid
    where timestampdiff(day,from_unixtime(o.updatedOn + 19800),from_unixtime(unix_timestamp())) >= 30
    group by 
    concat
    ) od1 on od1.concat = concat(vss.variantid,'_', vss.sizeid)
    where vss.quantity = 0
    order by pareto_rank desc limit 10 ''')

    print('Data Fetched')
    print('Making Dataframe')
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    print('Datframe Done')
    df.to_csv('sm_inventory.csv')
    print(df)


def import_git():


# Replace with your GitHub token, repository name, file path, and CSV content
    github_token = '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'
    repo_name = 'SupplyAnalytics/repository'
    file_path_in_repo = 'path/to/your_file.csv'
    local_csv_path = 'path/to/local_file.csv'
    commit_message = 'Add CSV file'

    # Authenticate to GitHub
    g = Github(github_token)
    repo = g.get_repo(repo_name)

    # Read the CSV file content
    with open(local_csv_path, 'r') as file:
        content = file.read()

    # Encode content to base64
    content_encoded = base64.b64encode(content.encode()).decode()

    # Create or update the file in the repository
    try:
        # Check if the file exists in the repo
        repo_file = repo.get_contents(file_path_in_repo)
        # If file exists, update it
        repo.update_file(repo_file.path, commit_message, content, repo_file.sha)
        print(f'File {file_path_in_repo} updated successfully.')
    except:
        # If file does not exist, create it
        repo.create_file(file_path_in_repo, commit_message, content)
        print(f'File {file_path_in_repo} created successfully.')


if __name__ == "__main__":
    connection()
