import pandas as pd
import streamlit as st
import numpy as np
from twelvedata import TDClient
from opensea import OpenseaAPI
import CustomModule as cm
from MCForecastTools import MCSimulation
from PIL import Image


# Streamlit UI
st.sidebar.header("Sort and Filter")
asset_categories = st.sidebar.selectbox("Assets", ['NFT', 'Cryptocurrencies'])
st.header(f"Crypto API Tracker - {asset_categories}")



# Opensea API Key
opensea_api = OpenseaAPI(apikey="7913a9c0377249d2998900d7ce6d38b3")


# Twelve Data API Key
td = TDClient(apikey="d1d0c43b0fb445518d1435c2b90c9cdc") 



# NFT Assets

# Main NFT Code
if asset_categories == 'NFT':
    
    filters = st.sidebar.selectbox("Filters", ['Statistics', 'Compare'])
    
    # Filter Selection
    # Statistics Filter
    if filters == 'Statistics':
        #User input Code
        st.subheader('Collection Contract Address')
        user_input_stats = str(st.text_input('What NFT Contract Address would you like to explore? ')) 
        
        # Check for user input
        if len(user_input_stats) > 1:
            
             # Contract Data
        
            contract_data = opensea_api.contract(asset_contract_address = user_input_stats)
            description = contract_data['collection']['description']
            date_of_creation = contract_data['collection']['created_date']
            discord = contract_data['collection']['discord_url']
            website = contract_data['collection']['external_url']
            name = (contract_data['collection']['name']).title()
            telegram = contract_data['collection']['telegram_url']
            twitter = contract_data['collection']['twitter_username']
            instagram = contract_data['collection']['instagram_username']
            address = contract_data['address']
            # Project Description
            st.subheader(f"{name}")
            st.subheader('Project Summary:')
            st.write(f'{description}')
            
            # Collection statistics
            st.subheader('Collection Statistics')
            user_input = user_input_stats
            st.write(cm.pull_nft_stats(user_input, opensea_api))
            
            # Project Socials
            st.write(cm.get_socials(name, telegram, twitter, instagram, discord, website))

        # Compare Filter
    elif filters == 'Compare':
        st.subheader("Comparing NFT Collections")
        user_input_compare_first = str(st.text_input("What is the first NFT collection you would like to compare?"))
        response_2 = ''
        user_input_compare_second = str(st.text_input("What is the second NFT collection you would like to compare?", key = response_2))
        
        # Checking for user input
        if len(user_input_compare_first) > 1:
            if len(user_input_compare_second) > 1:

                # Contract Data
                # First set of contract data
                contract_data_first = opensea_api.contract(asset_contract_address = user_input_compare_first)
                description1 = contract_data_first['collection']['description']
                date_of_creation1 = contract_data_first['collection']['created_date']
                discord1 = contract_data_first['collection']['discord_url']
                website1 = contract_data_first['collection']['external_url']
                name1 = (contract_data_first['collection']['name']).title()
                telegram1 = contract_data_first['collection']['telegram_url']
                twitter1 = contract_data_first['collection']['twitter_username']
                instagram1 = contract_data_first['collection']['instagram_username']
                address1 = contract_data_first['address']

                # Second set of Contract Data
                contract_data_second = opensea_api.contract(asset_contract_address = user_input_compare_second)
                description2 = contract_data_second['collection']['description']
                date_of_creation2 = contract_data_second['collection']['created_date']
                discord2 = contract_data_second['collection']['discord_url']
                website2 = contract_data_second['collection']['external_url']
                name2 = (contract_data_second['collection']['name']).title()
                telegram2 = contract_data_second['collection']['telegram_url']
                twitter2 = contract_data_second['collection']['twitter_username']
                instagram2 = contract_data_second['collection']['instagram_username']
                address2 = contract_data_second['address']

                # Creating two Columns for comparison
                col1, col2 = st.columns(2)

                # Defining the two columns
                with col1:
                    # Project Desciption
                    st.subheader(f'{name1}')
                    st.subheader('Project Summary')
                    st.write(f'{description1}')

                    # Collection 1 Statistics
                    st.subheader(f'{name1} Statistics')
                    user_input = user_input_compare_first
                    st.write(cm.pull_nft_stats(user_input, opensea_api ))
                
                with col2:
                    # Project Desciption
                    st.subheader(f'{name2}')
                    st.subheader('Project Summary')
                    st.write(f'{description2}')

                    # Collection 1 Statistics
                    st.subheader(f'{name2} Statistics')
                    user_input = user_input_compare_second
                    st.write(cm.pull_nft_stats(user_input, opensea_api))


# Cryptocurrency assets

# Code for Crypto DataFrame
# Defined Crypto Functions




# Cryptocurrency asset code
if asset_categories == "Cryptocurrencies":
    
    # Filters drop down with all the different types of Data
    filters = st.sidebar.selectbox("Primary Filters", ['Data Table', 'Percentage Change/Sharpe Ratio', 'Cumulative Returns',
    'Two Year Percentage Change/Sharpe Ratio', 'Two Year Cumulative Returns', 'Monte Carlo 5 Year', 'Monte Carlo 10 Year', 'Monte Carlo 20 Year'])
    
    # User imput code
    st.subheader('CryptoCurrency Ticker')
    user_inputc = st.text_input("What Crypto Currency Trading Pair are you looking for?")
    st.write("Ex: BTC/USD, ETH/USD, LUNAt/USD")
    
    #Checks to see if user has inputed a Crypto/USD pair
    if len(user_inputc) > 1:

    

        #Filter for Data Table
        if filters == "Data Table":
        
            # Executing the Crypto DataFrame
            st.header(f'{user_inputc} Data')
        
            st.write(cm.create_ts(user_inputc, td)) 
        

            # Define Data Frame
            crypto_df_new = cm.create_ts(user_inputc, td)
            crypto_df_close = crypto_df_new.drop(columns= ['open','high','low'])
            pct_change_raw = crypto_df_close.pct_change()
        
        #Filter for Percentage Change and Sharpe Ratio
        elif filters == "Percentage Change/Sharpe Ratio":
            
            #Defining Previous Data Frame for Pct_Change and Sharpe Ratios
            crypto_df_new = cm.create_ts(user_inputc, td)
            crypto_df_close = crypto_df_new.drop(columns= ['open','high','low'])
            pct_change_raw = crypto_df_close.pct_change()

            # Rename and assign pct_change_raw columns to pct_change 
            pct_change= pct_change_raw.rename(columns= {'close':'daily_return'}).dropna().copy()

            # Creating two Columns for comparison
            col1Pct, col2Sharpe = st.columns([2, 1])
            

            # Defining the two columns
            #Column 1 for Pct Change
            with col1Pct:
                # Pct Change Data
                st.subheader('Percentage Change')
                st.write(pct_change)

            #Column 2 for Sharpe Ratios
            with col2Sharpe:
                # Sharpe Ratio Data
                st.subheader('Sharpe Ratio')
                
                # Calculate annualized Standard Deviation
                std_annual = (pct_change.std()*np.sqrt(252))
            
                # Calculate annualized Mean Return
                mean_returns_annual = (pct_change.mean()*252)
            
                # Calculate annualized Sharpe Ratio
                sharpe_ratio = (mean_returns_annual/std_annual)
                st.write(sharpe_ratio)

            #Pct Change Graph
            st.subheader('Percentage Change Chart')
            #Line Chart for Percentage Change
            st.line_chart(pct_change, width=5000, height=200, use_container_width=True)
        
        #Filter for Cumulative Returns
        elif filters == "Cumulative Returns":

            #Defining Previous Data Frame, Pct_change and Sharpe Ratios for Cumulative Returns
            crypto_df_new = cm.create_ts(user_inputc, td)
            crypto_df_close = crypto_df_new.drop(columns= ['open','high','low'])
            pct_change_raw = crypto_df_close.pct_change()
            
            # Rename and assign pct_change_raw columns to pct_change 
            pct_change= pct_change_raw.rename(columns= {'close':'daily_return'}).dropna().copy()

            # Create cumulative returns subheader 
            st.subheader ('Cumulative Returns')

            # Calculate cumulative returns subheader 
            cumulative_returns = (1+pct_change).cumprod()
            st.write(cumulative_returns )
            st.line_chart(cumulative_returns, width=5000, height=200, use_container_width=True)

        # Filter for Two Year Percentage Change and Sharpe Ratio
        elif filters == "Two Year Percentage Change/Sharpe Ratio":

            #Sample Cryptocurrencies
            st.header('Sample Set of Cryptos(Last 2 Years)')

            #BTC, ETH, XRP, BNB, SOL, ADA and LUNA dataframe
            btc_df = (cm.btc_df)
            eth_df = (cm.eth_df)
            xrp_df = (cm.xrp_df)
            bnb_df = (cm.bnb_df)
            sol_df = (cm.sol_df)
            ada_df = (cm.ada_df)
            luna_df = (cm.luna_df)
            
            #Editing dataframe
            BTC1 = btc_df.drop(columns=['open', 'high', 'low'], axis=1)
            ETH1 = eth_df.drop(columns=['open', 'high', 'low'], axis=1)
            XRP = xrp_df.drop(columns=['open', 'high', 'low'], axis=1)
            BNB = bnb_df.drop(columns=['open', 'high', 'low'], axis=1)
            SOL = sol_df.drop(columns=['open', 'high', 'low'], axis=1)
            ADA = ada_df.drop(columns=['open', 'high', 'low'], axis=1)
            LUNA = luna_df.drop(columns=['open', 'high', 'low'], axis=1)           

            #Concatenate DFs, getting pct change, getting sharpe ratio, and posting the images of graphs
            custom_df= pd.concat([BTC1,ETH1,XRP,BNB,SOL,ADA,LUNA],axis=1, keys=['BTC/USD', 'ETH/USD', 'XRP/USD', 'BNB/USD', 'SOL/USD', 'ADA/USD', 'LUNA/USD'])
            custom_pct_change= custom_df.pct_change().dropna().copy()
            pic_pct = Image.open('pct.jpeg')
            st.subheader('Percentage Change')
            st.write(custom_pct_change)
            st.image(pic_pct)
            
            custom_sharpe_ratios = ((custom_pct_change.mean()) * 252) / (custom_pct_change.std() * np.sqrt(252))
            custom_sharpe_ratios = pd.DataFrame(custom_sharpe_ratios)
            st.subheader('Sharpe Ratios')
            st.write(custom_sharpe_ratios)
            pic_sharpe = Image.open('sharpe.jpeg')
            st.image(pic_sharpe)

        #Filter for Two Year Cumulative Returns
        elif filters == "Two Year Cumulative Returns":

            # Re-using data frame, percentage change and sharpe ratio from previous filter
            #BTC, ETH, XRP, BNB, SOL, ADA and LUNA dataframe
            btc_df = (cm.btc_df)
            eth_df = (cm.eth_df)
            xrp_df = (cm.xrp_df)
            bnb_df = (cm.bnb_df)
            sol_df = (cm.sol_df)
            ada_df = (cm.ada_df)
            luna_df = (cm.luna_df)
            
            #Editing dataframe
            BTC1 = btc_df.drop(columns=['open', 'high', 'low'], axis=1)
            ETH1 = eth_df.drop(columns=['open', 'high', 'low'], axis=1)
            XRP = xrp_df.drop(columns=['open', 'high', 'low'], axis=1)
            BNB = bnb_df.drop(columns=['open', 'high', 'low'], axis=1)
            SOL = sol_df.drop(columns=['open', 'high', 'low'], axis=1)
            ADA = ada_df.drop(columns=['open', 'high', 'low'], axis=1)
            LUNA = luna_df.drop(columns=['open', 'high', 'low'], axis=1)           

            #Concatenate DFs, getting pct change, getting sharpe ratio, and posting the images of graphs
            custom_df= pd.concat([BTC1,ETH1,XRP,BNB,SOL,ADA,LUNA],axis=1, keys=['BTC/USD', 'ETH/USD', 'XRP/USD', 'BNB/USD', 'SOL/USD', 'ADA/USD', 'LUNA/USD'])
            custom_pct_change= custom_df.pct_change().dropna().copy()
            
            custom_sharpe_ratios = ((custom_pct_change.mean()) * 252) / (custom_pct_change.std() * np.sqrt(252))
            custom_sharpe_ratios = pd.DataFrame(custom_sharpe_ratios)

            # Calculate cumulative returns subheader and post image of graph
            st.subheader('Cumulative Returns')
            custom_cumulative_returns = (1+custom_pct_change).cumprod()
            st.write(custom_cumulative_returns)
            cumulative_pic = Image.open('cumulative.jpeg')
            st.image(cumulative_pic)

        # Filter for 5 Year MonteCarlo Simulation
        elif filters == "Monte Carlo 5 Year":

            
            # Monte Carlo Simulation
            # Create BTC and ETH subheader for a Cryptocurrency Portfolio
                st.header('MonteCarlo Simulations')
                st.subheader('Sample Cryptocurrency Prices')
            # BTC and ETH DataFrame
                btc_df = (cm.btc_df)
                eth_df = (cm.eth_df)

            # Edit BTC and ETH DataFrame
                BTC =btc_df.drop(columns=['open', 'high', 'low'], axis=1)
                ETH= eth_df.drop(columns=['open', 'high', 'low'], axis=1)

            # Concatenate DFs
                portfolio_df= pd.concat([BTC,ETH],axis=1, keys=['BTC/USD', 'ETH/USD'])
                st.write(portfolio_df)

            # Configuring a Monte Carlo simulation to forecast 5 years cumulative returns
                MC_fiveyear = MCSimulation(
                    portfolio_data = portfolio_df,
                    weights = [.70,.30],
                    num_simulation = 500,
                    num_trading_days = 252*5
                    )
            # Running a Monte Carlo simulation to forecast 5 years cumulative returns
                st.subheader('Monte Carlo Simulation: 5yr')
                MC_fiveyear_calc = MC_fiveyear.calc_cumulative_return()
                st.write(MC_fiveyear_calc)

            # Plotting images of MC 5yr Simulation & Distribution
                sim_1260 = Image.open('1260_Simulation.jpeg')
                st.image(sim_1260)
                dist_1260 = Image.open('1260_distribution.jpeg')
                st.image(dist_1260)

            # Fetch summary statistics from the 5yr Monte Carlo simulation results
                st.subheader('Monte Carlo Simulation: 5yr Summary Statistics')
                summary_statistics_five = MC_fiveyear.summarize_cumulative_return()

            # Print summary statistics
                st.write(summary_statistics_five)


                # Set initial investment
                initial_investment = 20000
                st.subheader('Value of US$20,000 initial investment')
            # Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
                ci_lower = round(summary_statistics_five[8]*initial_investment,2)
                ci_upper = round(summary_statistics_five[9]*initial_investment,2)

            # Print results
                st.text(f'There is a 95% chance that an initial investment of ${initial_investment: 0.2f}'
                ' in the portfolio over the next 5 years will end within the range of'
                f' ${ci_lower: 0.2f} and ${ci_upper: 0.2f}')
        
        # Filter for 10 Year MonteCarlo Simulation
        elif filters == "Monte Carlo 10 Year":

            # Monte Carlo Simulation
            # Create BTC and ETH subheader for a Cryptocurrency Portfolio
                st.header('MonteCarlo Simulations')
                st.subheader('Sample Cryptocurrency Prices')
            # BTC and ETH DataFrame
                btc_df = (cm.btc_df)
                eth_df = (cm.eth_df)

            # Edit BTC and ETH DataFrame
                BTC =btc_df.drop(columns=['open', 'high', 'low'], axis=1)
                ETH= eth_df.drop(columns=['open', 'high', 'low'], axis=1)

            # Concatenate DFs
                portfolio_df= pd.concat([BTC,ETH],axis=1, keys=['BTC/USD', 'ETH/USD'])
                st.write(portfolio_df)

            # Configuring a Monte Carlo simulation to forecast 10 years cumulative returns
                MC_tenyear = MCSimulation(
                    portfolio_data = portfolio_df,
                    weights = [.70,.30],
                    num_simulation = 500,
                    num_trading_days = 252*10
                    )

            # Running a Monte Carlo simulation to forecast 10 years cumulative returns
                st.subheader('Monte Carlo Simulation: 10yr')
                MC_tenyear_calc = MC_tenyear.calc_cumulative_return()
                st.write(MC_tenyear_calc)

            # Plotting MC 10yr Simulation & Distribution
                sim_2520 = Image.open('2520_Simulations.jpeg')
                st.image(sim_2520)
                dist_2520 = Image.open('2520_distribution.jpeg')
                st.image(dist_2520)
            
            # Fetch summary statistics from the 10yr Monte Carlo simulation results
                st.subheader('Monte Carlo Simulation: 10yr Summary Statistics')
                summary_statistics_ten = MC_tenyear.summarize_cumulative_return()

            # Print summary statistics
                st.write(summary_statistics_ten)

            # Set initial investment
                initial_investment = 20000

            # Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
                ci_lower = round(summary_statistics_ten[8]*initial_investment,2)
                ci_upper = round(summary_statistics_ten[9]*initial_investment,2)

            # Print results
                st.text(f"There is a 95% chance that an initial investment of ${initial_investment}"
                        "in the portfolio over the next 10 years will end within in the range of"
                        f" ${ci_lower: 0.2f} and ${ci_upper: 0.2f}")

        # Filter for 20 Year MonteCarlo Simulation
        elif filters == "Monte Carlo 20 Year":

            # Monte Carlo Simulation
            # Create BTC and ETH subheader for a Cryptocurrency Portfolio
                st.header('MonteCarlo Simulations')
                st.subheader('Sample Cryptocurrency Prices')
            # BTC and ETH DataFrame
                btc_df = (cm.btc_df)
                eth_df = (cm.eth_df)

            # Edit BTC and ETH DataFrame
                BTC =btc_df.drop(columns=['open', 'high', 'low'], axis=1)
                ETH= eth_df.drop(columns=['open', 'high', 'low'], axis=1)

            # Concatenate DFs
                portfolio_df= pd.concat([BTC,ETH],axis=1, keys=['BTC/USD', 'ETH/USD'])
                st.write(portfolio_df)

            # Configuring a Monte Carlo simulation to forecast 20 years cumulative returns
                MC_twentyyear = MCSimulation(
                    portfolio_data = portfolio_df,
                    weights = [.70,.30],
                    num_simulation = 500,
                    num_trading_days = 252*20
                    )

            # Running a Monte Carlo simulation to forecast 20 years cumulative returns
                st.subheader('Monte Carlo Simulation: 20yr')
                MC_twentyyear_calc = MC_twentyyear.calc_cumulative_return()
                st.write(MC_twentyyear_calc)

            # Plotting 20yr Monte Carlo Simulation and Distribution
                sim_5040 = Image.open('5040_Simulations.jpeg')
                st.image(sim_5040)
                dist_5040 = Image.open('5040_distributions.jpeg')
                st.image(dist_5040)
            # Fetch summary statistics from the 20yr Monte Carlo simulation results
                st.subheader('Monte Carlo Simulation: 20yr Summary Statistics')
                summary_statistics_twenty = MC_twentyyear.summarize_cumulative_return()

            # Print summary statistics
                st.write(summary_statistics_twenty)

            # Set initial investment
                initial_investment = 20000

            # Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
                ci_lower = round(summary_statistics_twenty[8]*initial_investment,2)
                ci_upper = round(summary_statistics_twenty[9]*initial_investment,2)

            # Print results
                st.text(f"There is a 95% chance that an initial investment of ${initial_investment: 0.2f}"
                        "in the portfolio over the next 20 years will end within in the range of"
                    f" ${ci_lower:0.2f} and ${ci_upper:0.2f}")