import fundamentalanalysis as fa
import json
import financedatabase as fd


ticker = ["META"]
api_key = "1466dc09b9ed5e310e9161f7e826a822"
# inscope_companies = []


# Show the available companies
#companies = fa.available_companies(api_key)

#companies = [ "ETH", "GOGN", "000540.SZ", "603931.SS", "JMG.L", "067900.KS", "BSP.AX", "ERM.L", "LVCLY", "SBFMW", "CPAH", "JGLE.JK", "SMWN.DE", "0729.HK", "CYBN", "PLUGD", "0440.HK", "FVTID", "GOAU4.SA", "1930.HK", "CDTI", "PRCX", "688133.SS", "SCRM", "SHALPAINTS.NS", "ATZ.TO", "8187.HK", "1210.HK", "AMST", "603023.SS", "VRSN", "DFRG", "EMHTF", "ALO", "MEC", "CTAQU", "WFT.TO", "NFG", "300050.SZ", "BT-A.L", "8395.HK", "KLTR", "1815.T", "VSVS.L", "0771.HK", "LEAT", "PRO", "GZF.DE", "BDXA", "HRB", "002042.SZ", "AURCU", "AHNR", "TCT.ST", "7816.T", "GUL.AX", "UIHCU", "SRTS", "AQ", "ALAQU.PA", "THYCY", "GRX", "RAPT4.SA", "AUC.AX", "EC.PA", "BCI.TO", "MARUY", "TPVG", "MLIA.JK", "ORIA", "688767.SS", "BAYERCROP.NS", "002123.SZ", "WSR", "BWCXP", "XAM.AX", "601877.SS", "SRBANK.OL", "FFHL", "PRU.TO", "OBTC", "CLN.SW", "SLT.DE", "VLD", "EMR.AX", "CAP.PA", "QRMLF", "ZEV-WT", "LSYN", "VWAPY", "RVLV", "4100.T", "3924.T", "7606.T", "AXAC-RI", "GE.SW", "MIGI", "EQT.AX", "ARIES.NS", "DHCNL", "BLUECHIP.NS", "8616.T", "VII", "000972.SZ", "ADDERA.ST", "BONAS.ST", "600486.SS", "SYX", "TRVN", "DBL.NS", "1201.SR", "FRONW", "WINT", "CHI", "3032.TW", "ATC.AX", "CLBR", "6506.T", "CGEM", "NM", "SPG", "AI.TO", "603444.SS", "KYN", "2220.SR", "603363.SS", "MANAPPURAM.NS", "5363.T", "LTHM.L", "TCRI", "ASPO.HE", "LGACW", "0067.HK"]
#companies = [ "ETH", "GOGN", "JMG.L"]
#airlines_us = fd.select_equities(country='United States', industry='Airlines')
#eq_dk = fd.select_equities(country='Denmark')
#print(airlines_us.keys())
# finance_us = fd.select_equities(country='United States', sector='Financial Services')
#finance_us = fd.select_equities(country='United States', industry='Banks - Diversified')

us_industries = ['Advertising Agencies', 'Trucking']
equities_sectors = fd.show_options('equities', 'sectors')
sectors = ['Consumer Goods']


for sector in sectors:
    inscope_companies = []
    try:
        companies = fd.select_equities(country='United States', sector=sector)
    except AttributeError:
        pass
    else:
        for company in companies:
            try:
                ### Fetch API data ###
                quotes = fa.quote(company, api_key)
                profile = fa.profile(company, api_key)
                income_statement_annually = fa.income_statement(company, api_key, period="annual")
                balance_sheet_quarterly = fa.balance_sheet_statement(company, api_key, period="quarter")

                ### Variables ###
                market_cap = quotes.index.get_value(quotes, 'marketCap')[0]
                cash_equivalents = balance_sheet_quarterly.index.get_value(balance_sheet_quarterly, 'cashAndCashEquivalents')[0]
                cash_investments = balance_sheet_quarterly.index.get_value(balance_sheet_quarterly, 'cashAndShortTermInvestments')[0]
                total_curent_assets = balance_sheet_quarterly.index.get_value(balance_sheet_quarterly, 'totalCurrentAssets')[0]
                total_liabilities = balance_sheet_quarterly.index.get_value(balance_sheet_quarterly, 'totalLiabilities')[0]

                ### Calculated variables ###
                ncav_cash_equivalents = cash_equivalents - total_liabilities
                discount_cash_equivalents = market_cap / ncav_cash_equivalents

                ncav_total_current_assets = total_curent_assets - total_liabilities
                discount_total_current_assets = market_cap / ncav_total_current_assets

                ncav_cash_investments = cash_investments - total_liabilities
                discount_cash_investments = market_cap / ncav_cash_investments

                pe = quotes.index.get_value(quotes, 'pe')[0]
                net_income = income_statement_annually.index.get_value(income_statement_annually, 'netIncome')[0]

                if discount_total_current_assets > 0 and discount_total_current_assets < 0.7 and pe > 0 and net_income > 0:
                #if 1 == 1:
                    ### TEST ####
                    #print(quotes.index.get_value(quotes, 'price')[0])
                    #print(quotes.index.get_value(quotes, 'name')[0])
                    #print(quotes.index.get_value(quotes, 'symbol')[0])

                    inscope_companies.append({
                        ### Quote data ###
                        "symbol": quotes.index.get_value(quotes, 'symbol')[0],
                        "company_name": quotes.index.get_value(quotes, 'name')[0],
                        "stock_price": quotes.index.get_value(quotes, 'price')[0],
                        "exchange": quotes.index.get_value(quotes, 'exchange')[0],
                        "pe": pe,
                        "market_cap": market_cap,
                        "eps": quotes.index.get_value(quotes, 'eps')[0],
                        "Shares Outstanding": quotes.index.get_value(quotes, 'sharesOutstanding')[0],


                        ### Profile Data ###
                        "last_dividend": profile.index.get_value(profile, 'lastDiv')[0],
                        "currency": profile.index.get_value(profile, 'currency')[0],
                        "cik": profile.index.get_value(profile, 'cik')[0],
                        "isin": profile.index.get_value(profile, 'isin')[0],
                        "industry": profile.index.get_value(profile, 'industry')[0],
                        "sector": profile.index.get_value(profile, 'sector')[0],
                        "country": profile.index.get_value(profile, 'country')[0],


                        ### Income Data ###
                        "income_filling_date": income_statement_annually.index.get_value(income_statement_annually, 'fillingDate')[0],
                        "net_income": net_income,


                        ### Balance Sheet Data ###
                        "balance_filing_date": balance_sheet_quarterly.index.get_value(balance_sheet_quarterly, 'fillingDate')[0],
                        "cash_equivalents": cash_equivalents,
                        "cash_investments": cash_investments,
                        "total_curent_assets": total_curent_assets,
                        "total_liabilities": total_liabilities,
                        "ncav_cash_equivalents": ncav_cash_equivalents,
                        "ncav_cash_investments": ncav_cash_investments,
                        "ncav_total_current_assets": ncav_total_current_assets,
                        "discount_cash_equivalents": discount_cash_equivalents,
                        "discount_cash_investments": discount_cash_investments,
                        "discount_total_current_assets": discount_total_current_assets
                    })
            except (KeyError, TypeError, ZeroDivisionError):
                pass

    with open(sector + '.json', 'w') as fp:
        json.dump(inscope_companies, fp)


# #  Collect general company information
# profile = fa.profile(ticker, api_key)

# # Collect recent company quotes
# quotes = fa.quote(ticker, api_key)

# # Collect market cap and enterprise value
# entreprise_value = fa.enterprise(ticker, api_key)

# # Show recommendations of Analysts
# ratings = fa.rating(ticker, api_key)

# # Obtain DCFs over time
# dcf_annually = fa.discounted_cash_flow(ticker, api_key, period="annual")

# # Collect the Balance Sheet statements
# balance_sheet_annually = fa.balance_sheet_statement(ticker, api_key, period="annual")

# # Collect the Income Statements
# income_statement_annually = fa.income_statement(ticker, api_key, period="annual")

# # Collect the Cash Flow Statements
# cash_flow_statement_annually = fa.cash_flow_statement(ticker, api_key, period="annual")

# # Show Key Metrics
# key_metrics_annually = fa.key_metrics(ticker, api_key, period="annual")

# # Show a large set of in-depth ratios
# financial_ratios_annually = fa.financial_ratios(ticker, api_key, period="annual")

# # Show the growth of the company
# growth_annually = fa.financial_statement_growth(ticker, api_key, period="annual")

# # Download general stock data
# stock_data = fa.stock_data(ticker, period="ytd", interval="1d")

# # Download detailed stock data
# stock_data_detailed = fa.stock_data_detailed(ticker, api_key, begin="2000-01-01", end="2020-01-01")

# # Download dividend history
# dividends = fa.stock_dividend(ticker, api_key, begin="2000-01-01", end="2020-01-01")


#if discount > 0 and discount < 1:

