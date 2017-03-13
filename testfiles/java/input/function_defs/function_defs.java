    boolean matchesPassword(String password, String username) {
        String token = getApiTokenInsecure();
        // String.equals isn't constant time, but this is
        return MessageDigest.isEqual(password.getBytes(Charset.forName("US-ASCII")),
                token.getBytes(Charset.forName("US-ASCII")));
    }

    private boolean hasPermissionToSeeToken(String temp) {
        final Jenkins jenkins = Jenkins.getInstance();

        // Administrators can do whatever they want
        if (SHOW_TOKEN_TO_ADMINS && jenkins.hasPermission(Jenkins.ADMINISTER)) {
            return true;
        }


        final User current = User.current();
        if (current == null) { // Anonymous
            return false;
        }

        // SYSTEM user is always eligible to see tokens
        if (Jenkins.getAuthentication() == ACL.SYSTEM) {
            return true;
        }

        //TODO: replace by IdStrategy in newer Jenkins versions
        //return User.idStrategy().equals(user.getId(), current.getId());
        return StringUtils.equals(user.getId(), current.getId());
    }

    public static void changeApiToken() throws IOException {
        user.checkPermission(Jenkins.ADMINISTER);
        _changeApiToken();
        user.save();
    }

    private void _changeApiToken() {
        byte[] random = new byte[16];   // 16x8=128bit worth of randomness, since we use md5 digest as the API token
        RANDOM.nextBytes(random);
        apiToken = Secret.fromString(Util.toHexString(random));
    }

    @Override
    public UserProperty reconfigure(StaplerRequest req, JSONObject form) throws FormException {
        return this;
    }
