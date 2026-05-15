from django.core.exceptions import ValidationError


class GitHubURLMixin:
    GITHUB_DOMAINS = ['github.com', 'www.github.com']

    def clean_github_url(self):
        github_url = self.cleaned_data.get('github_url')
        if github_url:
            allowed = any(domain in github_url for domain in self.GITHUB_DOMAINS)
            if not allowed:
                raise ValidationError('Ссылка должна вести на GitHub')
        return github_url
