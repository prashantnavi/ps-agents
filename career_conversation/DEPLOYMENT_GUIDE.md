# 🚀 Hugging Face Spaces Deployment Guide

## Prerequisites

1. **Hugging Face Account**: Create an account at [huggingface.co](https://huggingface.co)
2. **OpenAI API Key**: Get your API key from [platform.openai.com](https://platform.openai.com)

## Step 1: Create a New Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Fill in the details:
   - **Space name**: `career-conversation-ai` (or your preferred name)
   - **License**: MIT
   - **SDK**: Gradio
   - **Hardware**: CPU Basic (free tier)
   - **Visibility**: Public or Private

## Step 2: Upload Files

Upload these files to your Hugging Face Space:

### Required Files:
- `app.py` - Main application file
- `requirements.txt` - Python dependencies
- `README.md` - Space description and documentation
- `.gitignore` - Git ignore rules

### Optional Files:
- `knowledge.db` - Pre-populated database (if you have one)
- `me/linkedin.pdf` - Sample resume (if you want to include one)

## Step 3: Set Environment Variables

1. Go to your Space settings
2. Navigate to "Variables and secrets"
3. Add the following environment variable:
   - **Name**: `OPENAI_API_KEY`
   - **Value**: Your OpenAI API key
   - **Type**: Secret

## Step 4: Configure Space Settings

In your Space settings, ensure:
- **SDK**: Gradio
- **SDK Version**: 4.44.0
- **App File**: app.py
- **Hardware**: CPU Basic (or upgrade if needed)

## Step 5: Deploy

1. Push your files to the Space repository
2. The Space will automatically build and deploy
3. Monitor the build logs for any errors
4. Once deployed, your app will be available at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

## File Structure

Your Space should have this structure:
```
career-conversation-ai/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── README.md             # Space documentation
├── .gitignore           # Git ignore rules
├── knowledge.db         # Database (optional)
└── me/                  # Sample data (optional)
    ├── linkedin.pdf
    └── summary.txt
```

## Testing Your Deployment

1. **Check Build Logs**: Ensure all dependencies install correctly
2. **Test Upload**: Try uploading a PDF resume
3. **Test Chat**: Ask questions to verify the AI is working
4. **Check Errors**: Monitor for any runtime errors

## Troubleshooting

### Common Issues:

1. **Import Errors**: Check that all dependencies are in `requirements.txt`
2. **API Key Issues**: Verify the environment variable is set correctly
3. **File Upload Issues**: Ensure PDF processing works correctly
4. **Memory Issues**: Consider upgrading hardware if needed

### Debug Steps:

1. Check the Space logs for error messages
2. Test locally first with `python app.py`
3. Verify all file paths are correct
4. Ensure environment variables are set

## Customization

### Modify the App:
- Update `app.py` to change functionality
- Modify `README.md` to update the Space description
- Add more example questions in the interface

### Add Features:
- File upload validation
- More conversation examples
- Better error handling
- Custom themes

## Security Notes

- Never commit API keys to the repository
- Use environment variables for sensitive data
- The `knowledge.db` file is public if included
- Consider data privacy implications

## Performance Optimization

- Use appropriate hardware tier for your needs
- Optimize database queries
- Implement caching where appropriate
- Monitor resource usage

## Support

If you encounter issues:
1. Check the Hugging Face Spaces documentation
2. Review the build logs
3. Test locally first
4. Ask for help in the Hugging Face community

---

**Your Career Conversation AI is now ready to help people with their career development! 🎉**
