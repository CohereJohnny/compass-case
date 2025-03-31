# Cohere Compass SDK Web Interface - UI Component Mapping

This document maps the current Flask templates to their corresponding VueJS components for the migration.

## Navigation Components

### Current: Navbar (All Templates)

The navigation bar appears at the top of all pages and includes links to:
- Home
- Indexes
- Chat
- API Explorer
- Documentation
- Settings

### Target: VueJS Components

- `AppHeader.vue`: Container component for the navigation
- `AppNavigation.vue`: Navigation links using Vue Router
- `NavLink.vue`: Individual navigation link component

## Home Page

### Current: index.html

The home page displays three cards with information about the main features:
- Indexes & Documents
- API Explorer
- Chat with your Documents

### Target: VueJS Components

- `HomePage.vue`: Main page component
- `FeatureCard.vue`: Reusable card component for features
- `AppLayout.vue`: Common layout wrapper

## Indexes Page

### Current: indexes.html

Displays a list of indexes with buttons for:
- View
- Search
- Chat
- Upload

And a "Create Index" button at the top.

### Target: VueJS Components

- `IndexesPage.vue`: Main container 
- `IndexesList.vue`: List of indexes
- `IndexListItem.vue`: Individual index with actions
- `ActionButton.vue`: Reusable button component

## Create Index Page

### Current: create_index.html

Form for creating a new index with:
- Index name input
- Max chunks per document input
- Submit button

### Target: VueJS Components

- `CreateIndexPage.vue`: Container component
- `CreateIndexForm.vue`: Form component
- `FormField.vue`: Reusable form field component
- `SubmitButton.vue`: Form submission button

## View Index Page

### Current: view_index.html

Displays details about a specific index:
- Index metadata
- List of documents
- Action buttons

### Target: VueJS Components

- `IndexDetailPage.vue`: Main container
- `IndexMetadata.vue`: Display index information
- `DocumentsList.vue`: List of documents
- `ActionButtonGroup.vue`: Group of action buttons

## Upload Document Page

### Current: upload.html

Form for uploading documents:
- File input
- Document ID field
- Advanced settings toggle
- PDF parsing strategy options
- Chunk size and overlap inputs

### Target: VueJS Components

- `UploadDocumentPage.vue`: Container component
- `UploadForm.vue`: Main form component
- `FileUpload.vue`: File input component
- `AdvancedSettings.vue`: Collapsible settings panel
- `FormSelect.vue`: Dropdown select component

## Search Page

### Current: search.html

Search interface with:
- Search input
- Results count selector
- Results display with document snippets

### Target: VueJS Components

- `SearchPage.vue`: Container component
- `SearchForm.vue`: Search input and controls
- `SearchResults.vue`: Results container
- `SearchResultItem.vue`: Individual result display
- `DocumentPreview.vue`: Modal for full document view

## Chat Page (Single Index)

### Current: chat.html

Chat interface for a specific index:
- Chat history display
- Message input
- Send button
- Search results panel
- Model badge showing current model

### Target: VueJS Components

- `ChatPage.vue`: Container component with route params
- `ChatHistory.vue`: Messages display
- `ChatMessage.vue`: Individual message 
- `ChatInput.vue`: Text input with send button
- `SearchContext.vue`: Context documents panel
- `ModelBadge.vue`: Display current model

## Chat Page (Multi-Index)

### Current: chat_index.html

Similar to single index chat but with:
- Index selector dropdown
- Welcome message

### Target: VueJS Components

- `MultiChatPage.vue`: Container component
- `IndexSelector.vue`: Dropdown for index selection
- (Reuse components from single chat interface)

## API Explorer

### Current: api_explorer.html

Interactive API testing interface:
- Client type selector
- Method selector
- Parameter form
- Execute button
- Response display
- Example code

### Target: VueJS Components

- `ApiExplorerPage.vue`: Container component
- `ClientSelector.vue`: Select client type
- `MethodSelector.vue`: Select method to call
- `ParameterForm.vue`: Dynamic form for parameters
- `ResponseDisplay.vue`: JSON response with formatting
- `CodeExample.vue`: Example code display with syntax highlighting

## Documentation Page

### Current: documentation.html

Documentation with:
- Section navigation
- Code examples
- SDK reference information

### Target: VueJS Components

- `DocumentationPage.vue`: Container component
- `DocSidebar.vue`: Navigation sidebar
- `DocSection.vue`: Individual documentation section
- `CodeBlock.vue`: Formatted code examples

## Settings Page

### Current: settings.html

Settings form with:
- Compass API token input
- Cohere API key input
- Chat model selector
- Save button

### Target: VueJS Components

- `SettingsPage.vue`: Container component
- `SettingsForm.vue`: Main form component
- `ApiKeyInput.vue`: Secure input with toggle visibility
- `ModelSelector.vue`: Model dropdown with metadata
- `SaveButton.vue`: Button with loading state

## Common Components

These components will be reused across multiple pages:

### Layout Components

- `AppLayout.vue`: Base layout with header and footer
- `PageHeader.vue`: Title and actions for each page
- `Sidebar.vue`: For pages that need a sidebar

### UI Elements

- `Card.vue`: Container with header and body
- `Button.vue`: Button with variants (primary, secondary, etc.)
- `Alert.vue`: Notification component
- `Spinner.vue`: Loading indicator
- `Modal.vue`: Dialog window
- `Tabs.vue`: Tabbed interface
- `Dropdown.vue`: Dropdown menu

### Form Components

- `TextInput.vue`: Text input field
- `SelectInput.vue`: Dropdown select
- `FileInput.vue`: File upload input
- `Toggle.vue`: Boolean toggle
- `RadioGroup.vue`: Radio button group
- `FormGroup.vue`: Label and input wrapper

## Component Hierarchy Example

Here's an example of the component hierarchy for the Chat page:

```
ChatPage.vue
├── AppLayout.vue
│   ├── AppHeader.vue
│   │   └── AppNavigation.vue
│   └── AppFooter.vue
├── PageHeader.vue
│   ├── ModelBadge.vue
│   └── Button.vue (Back button)
├── ChatContainer.vue
│   ├── ChatHistory.vue
│   │   └── ChatMessage.vue (Multiple)
│   └── ChatInput.vue
│       └── Button.vue (Send button)
└── SearchContextPanel.vue
    └── SearchResultItem.vue (Multiple)
        └── Modal.vue (Document preview)
```

## Styling Strategy

For migrating the styles:

1. **Base Styles**:
   - Continue using Bootstrap 5 for grid and utilities
   - Or migrate to a Vue component library like Vuetify or PrimeVue

2. **Component-Specific Styles**:
   - Use scoped CSS in Vue components
   - Extract common styles to shared files

3. **Theme Variables**:
   - Define CSS variables for colors, spacing, etc.
   - Support light/dark mode where applicable

## Responsive Design

All components should be designed with responsiveness in mind:

1. **Mobile-First Approach**:
   - Design for mobile first, then enhance for larger screens
   - Use Bootstrap's responsive grid or CSS Grid/Flexbox

2. **Breakpoints**:
   - Extra small: < 576px (mobile)
   - Small: ≥ 576px (mobile landscape/small tablet)
   - Medium: ≥ 768px (tablet)
   - Large: ≥ 992px (desktop)
   - Extra large: ≥ 1200px (large desktop)

3. **Component Adaptations**:
   - `ChatPage.vue`: Stack the chat and context panels on mobile
   - `IndexesList.vue`: Use a card layout on mobile instead of a table
   - `ApiExplorer.vue`: Simplify the layout on smaller screens

## Animation and Transitions

Consider adding the following animations:

1. **Page Transitions**:
   - Fade between routes
   - Slide transitions for related views

2. **Component Animations**:
   - Fade in/out for alerts and notifications
   - Slide for expandable panels
   - Scale for modals

3. **Loading States**:
   - Skeleton loading for lists and cards
   - Progress indicators for file uploads

## Accessibility Considerations

Ensure all components meet accessibility guidelines:

1. **Semantic HTML**:
   - Use appropriate elements (buttons, headings, etc.)
   - Maintain proper heading hierarchy

2. **ARIA Attributes**:
   - Add aria-labels to interactive elements
   - Use aria-live for dynamic content

3. **Keyboard Navigation**:
   - Ensure all interactions are keyboard accessible
   - Implement proper focus management

4. **Color Contrast**:
   - Maintain sufficient contrast for text and UI elements
   - Don't rely solely on color to convey information 