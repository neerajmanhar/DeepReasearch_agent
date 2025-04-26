import streamlit as st
import asyncio
from main import run_research_workflow

# Set page config
st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔍",
    layout="wide"
)

# Title and description
st.title("🔍 Research Assistant")
st.markdown("""
This tool helps you perform deep research on any topic using AI. 
Enter your query below and customize the search parameters.
""")

# Create the input form
with st.form("research_form"):
    # Query input
    query = st.text_area(
        "Enter your research query",
        placeholder="What would you like to research?",
        help="Be specific and clear in your query for better results"
    )
    
    # Create two columns for the sliders
    col1, col2 = st.columns(2)
    
    with col1:
        # Search type selection
        search_type = st.selectbox(
            "Search Type",
            options=["basic", "advanced"],
            help="Basic: Quick search with essential results\nAdvanced: Comprehensive search with detailed analysis"
        )
        
        # Max results slider
        max_results = st.slider(
            "Maximum Results",
            min_value=1,
            max_value=5,
            value=2,
            help="Number of results to include in the research (1-5)"
        )
    
    with col2:
        # Max tokens slider
        max_tokens = st.slider(
            "Maximum Output Length",
            min_value=256,
            max_value=2048,
            value=256,
            step=256,
            help="Maximum length of the output response (256-2048 tokens)"
        )
    
    # Submit button
    submit_button = st.form_submit_button("Start Research")

# Handle form submission
if submit_button and query:
    with st.spinner("Researching..."):
        # Run the research workflow
        result = asyncio.run(run_research_workflow(
            topic=query,
            search_type=search_type,
            max_results=max_results,
            max_tokens=max_tokens
        ))
        
        # Display results
        st.markdown("## Research Results")
        st.markdown(result["content"])
        
        # Replace the source display block with:
        if result["sources"]:
            st.markdown("### References")
            for source in result["sources"]:
                display_text = source['title'] if source['title'] != "Source" else "Source Document"
                st.markdown(f"- [{display_text}]({source['url']})")
            
elif submit_button:
    st.error("Please enter a research query.") 