import os

import pdfquery
import pandas as pd


def scrape():
    master = pd.DataFrame()
    for filename in os.scandir('input'):
        if filename.is_file():
            print(filename)
            pdf = pdfquery.PDFQuery(filename)
            pdf.load()
            #TODO: Don't need
            # pdf.tree.write('pdfXML.txt', pretty_print=True)
            shares = pdf.pq('LTTextLineHorizontal:overlaps_bbox("508.96, 675.037, 559.0, 684.037")').text()
            award_number = pdf.pq('LTTextLineHorizontal:overlaps_bbox("156.45, 654.107, 196.482, 663.107")').text()
            release_date = pdf.pq('LTTextLineHorizontal:overlaps_bbox("512.97, 685.497, 558.996, 694.497")').text()
            market_value = pdf.pq('LTTextLineHorizontal:overlaps_bbox("516.47, 664.567, 559.004, 673.567")').text()
            sale_price = pdf.pq('LTTextLineHorizontal:overlaps_bbox("516.47, 643.647, 559.004, 652.647")').text()
            shares_sold = pdf.pq('LTTextLineHorizontal:overlaps_bbox("217.14, 497.387, 255.66, 506.387")').text()
            page = pd.DataFrame({
                'filename': filename.name,
                'award_number': award_number,
                'release_date': release_date,
                'shares': shares.replace(',', ''),
                'market_value': market_value.replace('$', ''),
                'sale_price': sale_price.replace('$', ''),
                'shares_sold': shares_sold.replace('(', '').replace(')', '').replace(',', '')
            }, index=[0])
            master = master.append(page, ignore_index=True)
            # break
    master.to_csv('output.csv', index=False)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    scrape()
