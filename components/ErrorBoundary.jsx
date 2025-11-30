import React from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    // Log error details for debugging
    console.error('Error caught by boundary:', error, errorInfo);
    // Store error info in state for display
    this.setState({
      errorInfo: errorInfo
    });
  }

  getErrorMessage() {
    const { error } = this.state;
    if (!error && error !== false) return 'An unexpected error occurred';
    
    // Handle different error types
    if (error instanceof Error) {
      return error.message || 'An unexpected error occurred';
    }
    if (typeof error === 'string') {
      return error;
    }
    if (typeof error === 'boolean') {
      return error ? 'An error occurred (true)' : 'An error occurred (false)';
    }
    if (typeof error === 'number') {
      return `An error occurred (Error code: ${error})`;
    }
    if (error && typeof error === 'object' && 'message' in error) {
      return String(error.message);
    }
    return 'An unexpected error occurred';
  }

  getErrorStack() {
    const { error, errorInfo } = this.state;
    
    if (error instanceof Error && error.stack) {
      return error.stack;
    }
    if (errorInfo && errorInfo.componentStack) {
      return errorInfo.componentStack;
    }
    if (error && typeof error === 'object' && 'stack' in error) {
      return String(error.stack);
    }
    // For primitive types (boolean, number, string), show the error value
    if (error !== null && error !== undefined && (typeof error === 'boolean' || typeof error === 'number' || typeof error === 'string')) {
      return `Error value: ${String(error)}\n${errorInfo?.componentStack || 'No component stack available'}`;
    }
    return 'No stack trace available';
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-bg-main dark:bg-dark-bg-main flex items-center justify-center p-4">
          <div className="max-w-md w-full bg-bg-card dark:bg-dark-bg-card rounded-lg shadow-lg p-6 border border-gray-200 dark:border-dark-border">
            <h1 className="text-2xl font-bold text-text-heading dark:text-dark-text-primary mb-4">
              Something went wrong
            </h1>
            <p className="text-text-body dark:text-dark-text-secondary mb-4">
              {this.getErrorMessage()}
            </p>
            <button
              onClick={() => window.location.reload()}
              className="btn-primary"
            >
              Reload Page
            </button>
            <details className="mt-4">
              <summary className="cursor-pointer text-sm text-text-muted dark:text-dark-text-secondary">
                Error Details
              </summary>
              <pre className="mt-2 text-xs bg-gray-100 dark:bg-dark-bg-main p-2 rounded overflow-auto">
                {this.getErrorStack()}
              </pre>
            </details>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
