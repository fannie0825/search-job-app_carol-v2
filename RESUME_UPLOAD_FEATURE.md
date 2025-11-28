# Resume Upload & Auto-Extraction Feature

## 🎉 New Feature Added

The application now supports **automatic resume parsing** using semantic search! Instead of manually typing in your experience and education, you can simply upload your resume and let AI extract all the information.

## ✨ What's New

### Resume Upload
- Upload PDF, DOCX, or TXT resume files
- Automatic text extraction from uploaded files
- AI-powered semantic extraction of structured information

### Auto-Population
- Automatically fills in:
  - Name, email, phone, location
  - Professional summary
  - Work experience (with dates and achievements)
  - Education details
  - Skills list
  - Certifications and awards
  - LinkedIn and portfolio URLs (if mentioned)

## 🚀 How to Use

### Step 1: Upload Your Resume
1. Go to the **"My Profile"** tab
2. Scroll to the **"📄 Upload Your Resume"** section
3. Click **"Choose a resume file"**
4. Select your resume (PDF, DOCX, or TXT)

### Step 2: Extract Information
1. Click **"🔍 Extract Information from Resume"**
2. Wait for the AI to:
   - Extract text from your resume
   - Parse and structure the information
   - Populate your profile automatically

### Step 3: Review & Edit
1. Review the auto-filled information
2. Make any necessary edits
3. Click **"💾 Save Profile"**

## 🔧 Technical Details

### Supported File Formats
- **PDF** (.pdf) - Extracted using PyPDF2
- **Word Documents** (.docx, .doc) - Extracted using python-docx
- **Text Files** (.txt) - Direct text reading

### Extraction Process
1. **Text Extraction**: Reads text from uploaded file
2. **AI Parsing**: Uses Azure OpenAI GPT-4o-mini to:
   - Identify and extract structured information
   - Format experience with bullet points
   - Extract skills and certifications
   - Create professional summary
3. **Auto-Population**: Fills profile form automatically

### AI Extraction Prompt
The system uses a carefully crafted prompt to extract:
- Contact information (name, email, phone, location)
- Professional summary/objective
- Work experience (with dates, companies, achievements)
- Education (degrees, institutions, dates)
- Skills (technical and soft skills)
- Certifications, awards, publications
- Social links (LinkedIn, portfolio)

## 📋 Requirements

### New Dependencies
- `PyPDF2` - For PDF text extraction
- `python-docx` - For Word document text extraction

These are automatically installed when you run:
```bash
pip install -r requirements.txt
```

## 🎯 Benefits

1. **Time Saving**: No more manual data entry
2. **Accuracy**: AI extracts information precisely
3. **Consistency**: Structured format for all profiles
4. **Convenience**: Works with common resume formats
5. **Flexibility**: Still allows manual editing after extraction

## ⚠️ Notes

- The extraction works best with well-formatted resumes
- Some complex PDF layouts may require manual review
- Always review and verify extracted information
- You can still manually fill in the form if preferred
- Extraction requires Azure OpenAI API access

## 🔄 Workflow

```
Upload Resume → Extract Text → AI Parsing → Auto-Populate → Review & Edit → Save
```

## 💡 Tips for Best Results

1. **Use Standard Formats**: PDF or DOCX work best
2. **Clear Structure**: Well-organized resumes extract better
3. **Complete Information**: Include all sections (experience, education, skills)
4. **Review Always**: Check extracted data for accuracy
5. **Edit as Needed**: Make adjustments after extraction

---

**Status**: ✅ Feature implemented and ready to use!
